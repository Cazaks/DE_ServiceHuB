from rest_framework import serializers
from .models import Customer, Provider, ProviderAgreement


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone_number', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['id', 'user', 'phone_number', 'service_area', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']


class ProviderAgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderAgreement
        fields = ['id', 'provider', 'version', 'signed_at']
        read_only_fields = ['id', 'signed_at']
