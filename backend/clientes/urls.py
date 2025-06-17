from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, ContactoViewSet

router = DefaultRouter()
router.register(r'', ClienteViewSet)
router.register(r'contactos', ContactoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]