from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemViewSet

router = DefaultRouter()

router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'order_items', OrderItemViewSet, basename='order_items')

urlpatterns = router.urls