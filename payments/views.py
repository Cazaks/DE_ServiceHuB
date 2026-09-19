from rest_framework import viewsets
from .models import CustomerPayment, ProviderPayout
from .serializers import CustomerPaymentSerializer, ProviderPayoutSerializer


class CustomerPaymentViewSet(viewsets.ModelViewSet):
    queryset = CustomerPayment.objects.all()
    serializer_class = CustomerPaymentSerializer


class ProviderPayoutViewSet(viewsets.ModelViewSet):
    queryset = ProviderPayout.objects.all()
    serializer_class = ProviderPayoutSerializer