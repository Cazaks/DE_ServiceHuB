from django.contrib import admin
from .models import CustomerPayment, ProviderPayout

admin.site.register(CustomerPayment)
admin.site.register(ProviderPayout)