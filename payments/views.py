from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
import qrcode
import io
import base64
from .models import Merchant, PaymentLink, Payment, Buyer
from .serializers import (
    MerchantSerializer,
    PaymentLinkSerializer,
    PaymentSerializer,
    BuyerSerializer
)

class MerchantViewSet(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer

class PaymentLinkViewSet(viewsets.ModelViewSet):
    queryset = PaymentLink.objects.all()
    serializer_class = PaymentLinkSerializer

    def generate_qr_code(self, payment_link_id):
        """Generate QR code with payment link data"""
        payment_url = f"http://localhost:8008/pay/{payment_link_id}"
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(payment_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()

    def create(self, request, *args, **kwargs):
        """Create payment link with QR code"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        expiry_time = timezone.now() + timedelta(hours=24)
        payment_link = serializer.save(expiry_time=expiry_time)
        
        # Generate and save QR code
        qr_code = self.generate_qr_code(payment_link.id)
        payment_link.qr_code_data = qr_code
        payment_link.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def check_status(self, request, pk=None):
        """Check if payment link is still valid"""
        payment_link = self.get_object()
        
        if payment_link.status == PaymentLink.Status.EXPIRED:
            return Response({
                'status': 'expired',
                'message': 'This payment link has expired'
            })
        
        if payment_link.expiry_time and payment_link.expiry_time < timezone.now():
            payment_link.status = PaymentLink.Status.EXPIRED
            payment_link.save()
            return Response({
                'status': 'expired',
                'message': 'This payment link has expired'
            })
        
        return Response({
            'status': payment_link.status,
            'amount': payment_link.amount,
            'currency': payment_link.currency,
            'expires_at': payment_link.expiry_time
        })

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=False, methods=['post'])
    def process_payment(self, request):
        """Process a new payment"""
        payment_link_id = request.data.get('payment_link_id')
        buyer_data = request.data.get('buyer')
        
        # Get or create buyer
        buyer_serializer = BuyerSerializer(data=buyer_data)
        buyer_serializer.is_valid(raise_exception=True)
        buyer = buyer_serializer.save()
        
        # Get payment link
        payment_link = get_object_or_404(PaymentLink, id=payment_link_id)
        
        # Check if payment link is valid
        if payment_link.status != PaymentLink.Status.ACTIVE:
            return Response({
                'error': 'Payment link is not active'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create payment record
        payment_data = {
            'payment_link': payment_link.id,
            'buyer': buyer.id,
            'amount': payment_link.amount,
            'currency': payment_link.currency,
            'status': Payment.Status.PENDING
        }
        
        payment_serializer = self.get_serializer(data=payment_data)
        payment_serializer.is_valid(raise_exception=True)
        payment = payment_serializer.save()
        
        # Simulate payment processing
        # In real app, this would integrate with payment gateway
        try:
            self.simulate_payment_processing(payment)
            return Response({
                'status': 'success',
                'payment_id': payment.id,
                'message': 'Payment processed successfully'
            })
        except Exception as e:
            payment.status = Payment.Status.FAILED
            payment.save()
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def simulate_payment_processing(self, payment):
        """Simulate payment gateway processing"""
        # In real app, this would be replaced with actual payment gateway integration
        payment.status = Payment.Status.COMPLETED
        payment.paid_at = timezone.now()
        payment.transaction_reference = f"SIMULATED_TXN_{payment.id}"
        payment.save()
        
        # Update payment link status
        payment_link = payment.payment_link
        payment_link.status = PaymentLink.Status.COMPLETED
        payment_link.save()