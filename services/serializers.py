from rest_framework import serializers
from .models import ServiceCategory, ServiceRequest, ServiceOffer


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'holdback_days']
        read_only_fields = ['id']


class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ['id', 'customer', 'category', 'description', 'availability_window', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']


class ServiceOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOffer
        fields = ['id', 'request', 'quoted_price', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']