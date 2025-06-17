from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet,
    TallaViewSet,
    ColorViewSet,
    PrendaViewSet,
    VariantePrendaViewSet,
    ImagenPrendaViewSet
)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'tallas', TallaViewSet)
router.register(r'colores', ColorViewSet)
router.register(r'prendas', PrendaViewSet)
router.register(r'variantes', VariantePrendaViewSet)
router.register(r'imagenes', ImagenPrendaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]