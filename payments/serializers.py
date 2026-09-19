from rest_framework import serializers
from .models import CustomerPayment, ProviderPayout


class CustomerPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPayment
        fields = ['id', 'booking', 'amount', 'status', 'paid_at', 'created_at']
        read_only_fields = ['id', 'status', 'paid_at', 'created_at']


class ProviderPayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderPayout
        fields = [
            'id', 'assignment', 'initial_amount', 'holdback_amount',
            'release_due_date', 'status', 'initial_paid_at', 'released_at', 'created_at',
        ]
        read_only_fields = [
            'id', 'release_due_date', 'status', 'initial_paid_at', 'released_at', 'created_at',
        ]