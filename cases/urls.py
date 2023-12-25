from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CaseViewSet, FileViewSet

# Create a router and register your viewsets with it.
router = DefaultRouter()
router.register(r'cases', CaseViewSet, basename='case')
router.register(r'files', FileViewSet, basename='file')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
