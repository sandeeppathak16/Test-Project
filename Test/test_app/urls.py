from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlaceOrderAPIVeiwset, CurrentUserAPIViewSet

router = DefaultRouter()
router.register(r'orders', PlaceOrderAPIVeiwset, basename='order')
router.register(r'users', CurrentUserAPIViewSet, basename='user')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
