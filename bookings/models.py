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


class Assignee(models.Model):
    class AssigneeStatus(models.TextChoices):
        OFFERED = 'offered', 'Offered to provider'
        CONFIRMED = 'confirmed', 'Confirmed by provider'
        DECLINED = 'declined', 'Declined by provider'
        COMPLETED = 'completed', 'Job completed'

    booking = models.OneToOneField(Booking, on_delete=models.PROTECT, related_name='assignment')
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT, related_name='assignments')
    payout_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=25, choices=AssigneeStatus.choices, default=AssigneeStatus.OFFERED)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Assignment #{self.pk} - {self.provider} ({self.get_assignmentstatus_display()})'
