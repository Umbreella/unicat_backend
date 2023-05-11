from django.contrib import admin

from .models.Payment import Payment


@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    pass
