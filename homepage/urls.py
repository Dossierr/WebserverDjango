from django.urls import path
from .views import homepage  # Import your views from cases.views


urlpatterns = [
    path('', homepage, name='homepage'),
]