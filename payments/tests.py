from decimal import Decimal

from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Customer, Provider
from services.models import ServiceCategory, ServiceRequest, ServiceOffer
from bookings.models import Booking, Assignment
from .models import ProviderPayout
from django.utils import timezone

from django.core.exceptions import ValidationError


class ProviderPayoutReleaseDateTests(TestCase):
    def setUp(self):
        customer_user = User.objects.create_user(username='paycustomer', password='testpass123')
        customer = Customer.objects.create(user=customer_user, phone_number='08011112222')

        provider_user = User.objects.create_user(username='payprovider', password='testpass123')
        provider = Provider.objects.create(user=provider_user, phone_number='08033334444')

        category = ServiceCategory.objects.create(name='Test Cleaning', holdback_days=7)

        request = ServiceRequest.objects.create(
            customer=customer,
            category=category,
            description='Deep clean apartment',
            availability_window='Weekday mornings',
        )

        offer = ServiceOffer.objects.create(request=request, quoted_price='10000.00')
        self.booking = Booking.objects.create(offer=offer)

        assignment = Assignment.objects.create(
            booking=self.booking,
            provider=provider,
            payout_amount='7000.00',
        )

        self.payout = ProviderPayout.objects.create(
            assignment=assignment,
            initial_amount='4900.00',
            holdback_amount='2100.00',
        )

    def test_release_date_is_none_when_not_yet_confirmed(self):
        result = self.payout.calculate_release_due_date()
        self.assertIsNone(result)

    def test_negative_holdback_amount_is_rejected(self):
        self.payout.holdback_amount = Decimal('-100.00')
        with self.assertRaises(ValidationError):
            self.payout.full_clean()

    def test_release_date_adds_category_holdback_days(self):
        self.booking.customer_confirmed_at = timezone.now()
        self.booking.save()

        result = self.payout.calculate_release_due_date()
        expected = (self.booking.customer_confirmed_at + timezone.timedelta(days=7)).date()

        self.assertEqual(result, expected)