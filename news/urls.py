from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsViewSet, ImageViewSet

router = DefaultRouter()
router.register(r'news', NewsViewSet)
router.register(r'images', ImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
