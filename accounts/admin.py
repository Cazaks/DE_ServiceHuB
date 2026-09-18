from django.contrib import admin
from .models import Customer, Provider, ProviderAgreement

admin.site.register(Customer)
admin.site.register(Provider)
admin.site.register(ProviderAgreement)