from rest_framework import viewsets
from .models import ServiceCategory, ServiceRequest, ServiceOffer
from .serializers import ServiceCategorySerializer, ServiceRequestSerializer, ServiceOfferSerializer


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer


class ServiceRequestViewSet(viewsets.ModelViewSet):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer


class ServiceOfferViewSet(viewsets.ModelViewSet):
    queryset = ServiceOffer.objects.all()
    serializer_class = ServiceOfferSerializer