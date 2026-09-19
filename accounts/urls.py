from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    CustomerViewSet, ProviderViewSet, ProviderAgreementViewSet,
    RegisterCustomerView, RegisterProviderView,
)
from django.urls import path

router = DefaultRouter()
router.register('customers', CustomerViewSet)
router.register('providers', ProviderViewSet)
router.register('provider-agreements', ProviderAgreementViewSet)

urlpatterns = [
    path('register/customer/', RegisterCustomerView.as_view(), name='register-customer'),
    path('register/provider/', RegisterProviderView.as_view(), name='register-provider'),
    path('login/', obtain_auth_token, name='api-login'),
] + router.urls