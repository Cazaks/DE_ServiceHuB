from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Customer, Provider
from services.models import ServiceCategory, ServiceRequest, ServiceOffer
from .models import Booking, Assignment


class BookingStatusTests(TestCase):
    def setUp(self):
        customer_user = User.objects.create_user(username='bookcustomer', password='testpass123')
        self.customer = Customer.objects.create(user=customer_user, phone_number='08011112222')

        category = ServiceCategory.objects.create(name='Test Plumbing', holdback_days=14)

        request = ServiceRequest.objects.create(
            customer=self.customer,
            category=category,
            description='Leaking pipe',
            availability_window='Weekday afternoons',
        )

        self.offer = ServiceOffer.objects.create(request=request, quoted_price='15000.00')

    def test_new_booking_starts_awaiting_assignment(self):
        booking = Booking.objects.create(offer=self.offer)
        self.assertEqual(booking.status, Booking.BookingStatus.AWAITING_ASSIGNMENT)

    def test_new_booking_has_no_assignment_yet(self):
        booking = Booking.objects.create(offer=self.offer)
        self.assertFalse(hasattr(booking, 'assignment'))


class AssignmentTests(TestCase):
    def setUp(self):
        customer_user = User.objects.create_user(username='bookcustomer2', password='testpass123')
        customer = Customer.objects.create(user=customer_user, phone_number='08011112223')

        provider_user = User.objects.create_user(username='bookprovider', password='testpass123')
        self.provider = Provider.objects.create(user=provider_user, phone_number='08033334444')

        category = ServiceCategory.objects.create(name='Test Electrical', holdback_days=30)

        request = ServiceRequest.objects.create(
            customer=customer,
            category=category,
            description='Faulty wiring',
            availability_window='Weekend mornings',
        )

        offer = ServiceOffer.objects.create(request=request, quoted_price='20000.00')
        self.booking = Booking.objects.create(offer=offer)

    def test_assigning_a_provider_creates_assignment_with_offered_status(self):
        assignment = Assignment.objects.create(
            booking=self.booking,
            provider=self.provider,
            payout_amount='14000.00',
        )
        self.assertEqual(assignment.status, Assignment.AssignmentStatus.OFFERED)

    def test_booking_can_access_its_assignment_once_created(self):
        Assignment.objects.create(
            booking=self.booking,
            provider=self.provider,
            payout_amount='14000.00',
        )
        self.assertTrue(hasattr(self.booking, 'assignment'))