from django.contrib import admin

from django_tbank_kassa import models


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'created_at',
        'amount',
        'id',
        'status',
    ]
    readonly_fields = [
        'id',
        'created_at',
        'amount',
        'status',
        'payment_id',
        'payment_url',
    ]
