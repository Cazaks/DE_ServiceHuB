from django.db import models
from accounts.models import Customer, Provider


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    holdback_days = models.PositiveBigIntegerField(default=7)

    def __str__(self):
        return self.name

class ServiceRequest(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = 'submitted', 'Submitted'
        INSPECTED = 'inspected', 'Inspected'
        QUOTED = 'quoted', 'Quoted'
        CLOSED = 'closed', 'Closed'

    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE, related_name='requests')
    category = models.ForeignKey(ServiceCategory,
                                 on_delete=models.PROTECT, related_name='requests')
    description = models.TextField()
    availability_window = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Request #{self.pk} - {self.customer} ({self.category})'

class ServiceOffer(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending customer response'
        ACCEPTED = 'accepted', 'Accepted'
        DECLINED = 'declined', 'Declined'

    request = models.OneToOneField(ServiceRequest, on_delete=models.CASCADE, related_name='offer')
    quoted_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Offer for request #{self.request.pl} - {self.quoted_price}'