from django.contrib import admin
from .models import Merchant, Payment, PaymentLink, Buyer

admin.site.register(Merchant)
admin.site.register(PaymentLink)
admin.site.register(Payment)
admin.site.register(Buyer)