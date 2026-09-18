from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from accounts.models import Customer
from .models import ServiceCategory, ServiceRequest
from django.db import connection

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