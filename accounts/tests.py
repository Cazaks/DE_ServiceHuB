from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Customer, Provider
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


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


class CustomerViewSetPermissionTests(APITestCase):
    def setUp(self):
        admin = User.objects.create_superuser(username='admin1', password='pass12345')
        self.admin_token = Token.objects.create(user=admin)

        cust_user = User.objects.create_user(username='cust1', password='pass12345')
        self.customer = Customer.objects.create(user=cust_user, phone_number='08011112222')
        self.customer_token = Token.objects.create(user=cust_user)

        prov_user = User.objects.create_user(username='prov1', password='pass12345')
        Provider.objects.create(user=prov_user, phone_number='08033334444')
        self.provider_token = Token.objects.create(user=prov_user)

    def test_admin_sees_all_customers(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')
        response = self.client.get('/api/accounts/customers/')
        self.assertEqual(len(response.data), 1)

    def test_provider_sees_no_customers(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.provider_token.key}')
        response = self.client.get('/api/accounts/customers/')
        self.assertEqual(len(response.data), 0)

    def test_customer_sees_only_own_record(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        response = self.client.get('/api/accounts/customers/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.customer.id)

    def test_anonymous_request_is_rejected(self):
        response = self.client.get('/api/accounts/customers/')
        self.assertEqual(response.status_code, 401)


class ProviderViewSetPermissionTests(APITestCase):
    def setUp(self):
        admin = User.objects.create_superuser(username='admin2', password='pass12345')
        self.admin_token = Token.objects.create(user=admin)

        cust_user = User.objects.create_user(username='cust2', password='pass12345')
        Customer.objects.create(user=cust_user, phone_number='08011112223')
        self.customer_token = Token.objects.create(user=cust_user)

        prov_user = User.objects.create_user(username='prov2', password='pass12345')
        self.provider = Provider.objects.create(user=prov_user, phone_number='08033334445')
        self.provider_token = Token.objects.create(user=prov_user)

    def test_admin_sees_all_providers(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')
        response = self.client.get('/api/accounts/providers/')
        self.assertEqual(len(response.data), 1)

    def test_customer_sees_no_providers(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        response = self.client.get('/api/accounts/providers/')
        self.assertEqual(len(response.data), 0)

    def test_provider_sees_only_own_record(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.provider_token.key}')
        response = self.client.get('/api/accounts/providers/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.provider.id)


