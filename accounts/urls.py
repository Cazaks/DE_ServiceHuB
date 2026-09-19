from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, ProviderViewSet, ProviderAgreementViewSet

router = DefaultRouter()
router.register('customers', CustomerViewSet)
router.register('providers', ProviderViewSet)
router.register('provider-agreements', ProviderAgreementViewSet)

urlpatterns = router.urls