from decimal import Decimal

from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Customer, Provider
from services.models import ServiceCategory, ServiceRequest, ServiceOffer
from bookings.models import Booking, Assignment
from .models import ProviderPayout
from django.utils import timezone

from django.core.exceptions import ValidationError

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


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


class ProviderPayoutViewSetPermissionTests(APITestCase):
    def setUp(self):
        admin = User.objects.create_superuser(username='payadmin', password='pass12345')
        self.admin_token = Token.objects.create(user=admin)

        cust_user = User.objects.create_user(username='paycust', password='pass12345')
        customer = Customer.objects.create(user=cust_user, phone_number='08022220001')

        prov_user = User.objects.create_user(username='payprov', password='pass12345')
        self.provider = Provider.objects.create(user=prov_user, phone_number='08022220002')
        self.provider_token = Token.objects.create(user=prov_user)

        other_prov_user = User.objects.create_user(username='payprov2', password='pass12345')
        Provider.objects.create(user=other_prov_user, phone_number='08022220003')
        self.other_provider_token = Token.objects.create(user=other_prov_user)

        category = ServiceCategory.objects.create(name='Test Pay Category', holdback_days=7)
        request = ServiceRequest.objects.create(
            customer=customer, category=category,
            description='Test', availability_window='Anytime',
        )
        offer = ServiceOffer.objects.create(request=request, quoted_price='5000.00')
        booking = Booking.objects.create(offer=offer)
        self.assignment = Assignment.objects.create(
            booking=booking, provider=self.provider, payout_amount='3500.00',
        )
        self.payout = ProviderPayout.objects.create(
            assignment=self.assignment, initial_amount='2450.00', holdback_amount='1050.00',
        )

    def test_provider_cannot_create_payout(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.provider_token.key}')
        response = self.client.post('/api/payments/provider-payouts/', {
            'assignment': self.assignment.id,
            'initial_amount': '2450.00',
            'holdback_amount': '1050.00',
        })
        self.assertEqual(response.status_code, 403)

    def test_owner_provider_sees_own_payout(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.provider_token.key}')
        response = self.client.get('/api/payments/provider-payouts/')
        self.assertEqual(len(response.data), 1)

    def test_other_provider_sees_no_payouts(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.other_provider_token.key}')
        response = self.client.get('/api/payments/provider-payouts/')
        self.assertEqual(len(response.data), 0)

    def test_admin_sees_all_payouts(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')
        response = self.client.get('/api/payments/provider-payouts/')
        self.assertEqual(len(response.data), 1)