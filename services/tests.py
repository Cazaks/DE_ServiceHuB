from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from accounts.models import Customer
from .models import ServiceCategory, ServiceRequest, ServiceOffer
from django.db import connection
from decimal import Decimal
from django.core.exceptions import ValidationError

class ServiceCategoryLookupTests(TestCase):
    def test_looking_up_nonexistent_category_raises_does_not_exist(self):
        with self.assertRaises(ServiceCategory.DoesNotExist):
            ServiceCategory.objects.get(pk=9999)


class ServiceRequestForeignKeyTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='fkcustomer', password='testpass123')
        self.customer = Customer.objects.create(user=self.user, phone_number='08011112222')

    def test_creating_request_with_nonexistent_category_id_fails(self):
        request = ServiceRequest(
            customer=self.customer,
            category_id=9999,
            description='Leaking pipe',
            availability_window='Weekday afternoons',
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                request.save()
                connection.check_constraints()


class ServiceOfferValidationTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='offercustomer', password='testpass123')
        customer = Customer.objects.create(user=user, phone_number='08099998888')
        category = ServiceCategory.objects.create(name='Test Tiling', holdback_days=14)
        self.request = ServiceRequest.objects.create(
            customer=customer,
            category=category,
            description='Floor tiling',
            availability_window='Weekend',
        )

    def test_negative_quoted_price_is_rejected(self):
        offer = ServiceOffer(request=self.request, quoted_price=Decimal('-500.00'))
        with self.assertRaises(ValidationError):
            offer.full_clean()