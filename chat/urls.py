from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatViewSet

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r'chat', ChatViewSet, basename='chat')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
