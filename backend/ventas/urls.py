from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VentaViewSet, DevolucionViewSet

router = DefaultRouter()
router.register(r'', VentaViewSet)
router.register(r'devoluciones', DevolucionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]