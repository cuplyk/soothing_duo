from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'posts', api_views.PostViewSet, basename='post')
router.register(r'categories', api_views.CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]