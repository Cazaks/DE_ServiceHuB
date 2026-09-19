from rest_framework import serializers
from .models import Customer, Provider, ProviderAgreement, phone_validator, validate_not_blank
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.core.exceptions import ValidationError as DjangoValidationError


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

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(validators=[phone_validator])

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists')

        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')

        return value

    def validate_password(self, value):
        try:
            django_validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))

        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return Customer.objects.create(user=user, phone_number=validated_data['phone_number'])


class ProviderRegistrationSerializer(serializers.ModelSerializer):
    class ProviderSerializer(serializers.ModelSerializer):
        class Meta:
            model = Provider
            fields = ['id', 'user', 'phone_number', 'service_area', 'qualified_categories', 'status', 'created_at']
            read_only_fields = ['id', 'status', 'created_at']


    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(validators=[phone_validator])
    service_area = serializers.CharField()

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def validate_password(self, value):
        try:
            django_validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            service_area=validated_data['service_area']
        )
