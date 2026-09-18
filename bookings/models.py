from django.db import models
from accounts.models import Provider
from services.models import ServiceOffer

class Booking(models.Model):
    class BookingStatus(models.TextChoices):
        AWAITING_ASSIGNMENT = 'awaiting_assignment', 'Awaiting provider assignment'
        ASSIGNED = 'assigned', 'Provider assigned'
        IN_PROGRESS = 'in-progress', 'In progress'
        COMPLETED = 'completed', 'Completed'
        CANCELED = 'canceled', 'Canceled'

    offer = models.OneToOneField(ServiceOffer, on_delete=models.PROTECT, related_name='booking')
    status = models.CharField(max_length=25, choices=BookingStatus.choices, default=BookingStatus.AWAITING_ASSIGNMENT)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    customer_confirmed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Booking #{self.pk} - {self.get_bookingstatus_display()}'
