from rest_framework.routers import DefaultRouter
from .views import ServiceCategoryViewSet, ServiceRequestViewSet, ServiceOfferViewSet

router = DefaultRouter()
router.register('categories', ServiceCategoryViewSet)
router.register('requests', ServiceRequestViewSet, basename='servicerequest')
router.register('offers', ServiceOfferViewSet, basename='serviceoffer')

urlpatterns = router.urls