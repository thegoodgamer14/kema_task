from django.db import models
from django.utils import timezone
import uuid

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(editable=True)
    updated_at = models.DateTimeField(editable=True)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract=True

class Merchant(BaseModel):
    business_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=12)

    def __str__(self):
        return self.business_name

class PaymentLink(BaseModel):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        EXPIRED = 'EXPIRED', 'Expired'
        COMPLETED = 'COMPLETED', 'Completed'
    
    merchant = models.ForeignKey(
        Merchant,
        on_delete=models.PROTECT,
        related_name='payment_links'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Amount to be paid"
    )
    currency = models.CharField(
        max_length=3,
        default='AED',
        help_text="3-letter currency code"
    )
    description=models.TextField(blank=True)
    status=models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )
    qr_code_data = models.TextField(
        help_text="Data encoded in QR Code"
    )
    expiry_time=models.DateTimeField(
        null=True,
        blank=True,
        help_text="When this payment link expires"
    )

    def __str__(self):
        return f"{self.merchant.business_name} - {self.currency} {self.amount}"

class Buyer(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name

class Payment(BaseModel):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'
        REFUNDED = 'REFUNDED', 'Refunded'
    
    payment_link = models.ForeignKey(
        PaymentLink,
        on_delete=models.PROTECT,
        related_name='payments'
    )
    buyer = models.ForeignKey(
        Buyer,
        on_delete=models.PROTECT,
        related_name='payments'
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    transaction_reference = models.CharField(
        max_length=100,
        blank=True,
        help_text="Reference from payment gateway"
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the payment was successfully processed"
    )

    def __str__(self):
        return f"{self.buyer.name} - {self.currency} {self.amount}"
    
    class Meta:
        ordering = ['-created_at']