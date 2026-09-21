from decimal import Decimal
from datetime import timedelta
from django.db import models
from django.core.validators import MinValueValidator
from bookings.models import Booking, Assignment


class CustomerPayment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PAID = 'paid', 'Paid'
        REFUNDED = 'refunded', 'Refunded'

    booking = models.OneToOneField(Booking, on_delete=models.PROTECT, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def customer(self):
        return self.booking.customer

    def __str__(self):
        return f'Payment for Booking #{self.booking.pk} — {self.amount} ({self.get_status_display()})'

class ProviderPayout(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        INITIAL_PAID = 'initial_paid', 'Initial portion paid'
        HELD_FOR_REDO = 'held_for_redo', 'Held — funding a redo'
        RELEASED = 'released', 'Holdback released'
        FORFEITED = 'forfeited', 'Holdback forfeited'

    assignment = models.OneToOneField(Assignment, on_delete=models.PROTECT, related_name='payout')
    initial_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    holdback_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    release_due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    initial_paid_at = models.DateTimeField(null=True, blank=True)
    released_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_release_due_date(self):
        booking = self.assignment.booking
        confirmed_at = booking.customer_confirmed_at
        if confirmed_at is None:
            return None
        holdback_days = booking.offer.request.category.holdback_days
        return (confirmed_at + timedelta(days=holdback_days)).date()

    @property
    def provider(self):
        return self.assignment.provider

    def __str__(self):
        return f'Payout for Assignment #{self.assignment.pk} — {self.get_status_display()}'