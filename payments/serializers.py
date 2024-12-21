from rest_framework import serializers
from .models import Merchant, PaymentLink, Payment, Buyer
from django.utils import timezone

class BaseModelSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, default=serializers.CreateOnlyDefault(timezone.now))
    updated_at = serializers.DateTimeField(read_only=True)

class MerchantSerializer(BaseModelSerializer):
    class Meta:
        model = Merchant
        fields = '__all__'

class PaymentLinkSerializer(BaseModelSerializer):
    qr_code_data = serializers.CharField(read_only=True)
    class Meta:
        model = PaymentLink
        fields = '__all__'

class PaymentSerializer(BaseModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class BuyerSerializer(BaseModelSerializer):
    class Meta:
        model = Buyer
        fields = '__all__'