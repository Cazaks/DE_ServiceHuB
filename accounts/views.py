from rest_framework import viewsets
from .models import Customer, Provider, ProviderAgreement
from .serializers import CustomerSerializer, ProviderSerializer, ProviderAgreementSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class ProviderAgreementViewSet(viewsets.ModelViewSet):
    queryset = ProviderAgreement.objects.all()
    serializer_class = ProviderAgreementSerializer