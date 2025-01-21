from rest_framework import serializers

from django_tbank_kassa import models


class Payment(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = [
            'id',
            'created_at',
            'amount',
            'status',
            'payment_id',
            'payment_url',
        ]
        read_only_fields = [
            'created_at',
            'status',
            'payment_id',
            'payment_url',
        ]
