from django.contrib import admin
from .models import ServiceCategory, ServiceRequest, ServiceOffer

admin.site.register(ServiceCategory)
admin.site.register(ServiceRequest)
admin.site.register(ServiceOffer)