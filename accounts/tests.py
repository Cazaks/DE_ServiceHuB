from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Customer, Provider


class CustomerModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testcustomer', password='testpass123')

    def test_customer_created_with_valid_phone(self):
        customer = Customer.objects.create(user=self.user, phone_number='08012345678')
        self.assertEqual(customer.phone_number, '08012345678')

    def test_customer_str_shows_username_when_no_full_name(self):
        customer = Customer.objects.create(user=self.user, phone_number='08012345678')
        self.assertEqual(str(customer), 'testcustomer')

    def test_invalid_phone_number_is_rejected(self):
        customer = Customer(user=self.user, phone_number='abc')
        with self.assertRaises(ValidationError):
            customer.full_clean()


class ProviderModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testprovider', password='testpass123')

    def test_provider_defaults_to_pending_status(self):
        provider = Provider.objects.create(user=self.user, phone_number='08087654321')
        self.assertEqual(provider.status, Provider.Status.PENDING)

    def test_whitespace_only_service_area_is_rejected(self):
        provider = Provider(user=self.user, phone_number='08087654321', service_area='   ')
        with self.assertRaises(ValidationError):
            provider.full_clean()


class PasswordHashingTests(TestCase):
    def test_password_is_not_stored_as_plain_text(self):
        user = User.objects.create_user(username='hashcheck', password='testpass123')
        self.assertNotEqual(user.password, 'testpass123')

    def test_stored_password_uses_correct_algorithm_prefix(self):
        user = User.objects.create_user(username='hashcheck2', password='testpass123')
        self.assertTrue(user.password.startswith('pbkdf2_sha256$'))

    def test_check_password_validates_correct_password(self):
        user = User.objects.create_user(username='hashcheck3', password='testpass123')
        self.assertTrue(user.check_password('testpass123'))

    def test_check_password_rejects_wrong_password(self):
        user = User.objects.create_user(username='hashcheck4', password='testpass123')
        self.assertFalse(user.check_password('wrongpassword'))


