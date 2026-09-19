from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .models import Customer, Provider, ProviderAgreement
from .serializers import (
    CustomerSerializer, ProviderSerializer, ProviderAgreementSerializer,
    CustomerRegistrationSerializer, ProviderRegistrationSerializer,
)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class ProviderAgreementViewSet(viewsets.ModelViewSet):
    queryset = ProviderAgreement.objects.all()
    serializer_class = ProviderAgreementSerializer


class RegisterCustomerView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomerRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        token, _ = Token.objects.get_or_create(user=customer.user)
        return Response({'token': token.key, 'customer_id': customer.id}, status=status.HTTP_201_CREATED)


class RegisterProviderView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ProviderRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = serializer.save()
        token, _ = Token.objects.get_or_create(user=provider.user)
        return Response({'token': token.key, 'provider_id': provider.id}, status=status.HTTP_201_CREATED)