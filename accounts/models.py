from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

phone_validator = RegexValidator(
    regex = r'^\+?1?\d{9,15}$',
    message = 'Enter a valid phone number (10 - 15 digits, optionally starting with +).'
)

def validate_not_blank(value):
    if value and not value.strip():
        raise ValidationError('This field cannot be blank.')

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, validators=[phone_validator])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Provider(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending review'
        ACTIVE = 'active', 'Active'
        SUSPENDED = 'suspended', 'Suspended'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, validators=[phone_validator])
    service_area = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20,
                              choices=Status.choices,
                              default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class ProviderAgreement(models.Model):
    provider = models.OneToOneField(Provider, on_delete=models.CASCADE,
                                    related_name='agreement')
    vision = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Agreement v{self.vision} - {self.provider}"


