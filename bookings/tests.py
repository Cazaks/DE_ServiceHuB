from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Customer, Provider
from services.models import ServiceCategory, ServiceRequest, ServiceOffer
from .models import Booking, Assignment
from decimal import Decimal
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

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

    def test_negative_payout_amount_is_rejected(self):
        assignment = Assignment(
            booking=self.booking,
            provider=self.provider,
            payout_amount=Decimal('-1000.00'),
        )
        with self.assertRaises(ValidationError):
            assignment.full_clean()

class BookingViewSetPermissionTests(APITestCase):
    def setUp(self):
        admin = User.objects.create_superuser(username='bkadmin', password='pass12345')
        self.admin_token = Token.objects.create(user=admin)

        cust_user = User.objects.create_user(username='bkcust', password='pass12345')
        self.customer = Customer.objects.create(user=cust_user, phone_number='08011110001')
        self.customer_token = Token.objects.create(user=cust_user)

        other_cust_user = User.objects.create_user(username='bkcust2', password='pass12345')
        Customer.objects.create(user=other_cust_user, phone_number='08011110002')
        self.other_customer_token = Token.objects.create(user=other_cust_user)

        category = ServiceCategory.objects.create(name='Test BK Category', holdback_days=7)
        request = ServiceRequest.objects.create(
            customer=self.customer, category=category,
            description='Test', availability_window='Anytime',
        )
        offer = ServiceOffer.objects.create(request=request, quoted_price='5000.00')
        self.booking = Booking.objects.create(offer=offer)

    def test_customer_cannot_create_booking(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        offer2 = ServiceOffer.objects.create(
            request=ServiceRequest.objects.create(
                customer=self.customer, category=ServiceCategory.objects.first(),
                description='Another', availability_window='Anytime',
            ),
            quoted_price='6000.00',
        )
        response = self.client.post('/api/bookings/bookings/', {'offer': offer2.id})
        self.assertEqual(response.status_code, 403)

    def test_admin_can_create_booking(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')
        offer2 = ServiceOffer.objects.create(
            request=ServiceRequest.objects.create(
                customer=self.customer, category=ServiceCategory.objects.first(),
                description='Another', availability_window='Anytime',
            ),
            quoted_price='6000.00',
        )
        response = self.client.post('/api/bookings/bookings/', {'offer': offer2.id})
        self.assertEqual(response.status_code, 201)

    def test_owner_customer_sees_own_booking(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        response = self.client.get('/api/bookings/bookings/')
        self.assertEqual(len(response.data), 1)

    def test_other_customer_sees_no_bookings(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.other_customer_token.key}')
        response = self.client.get('/api/bookings/bookings/')
        self.assertEqual(len(response.data), 0)