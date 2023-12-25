# users/urls.py
from django.urls import path
from .views import CustomAuthToken

urlpatterns = [
    path('token-auth/', CustomAuthToken.as_view(), name='authtoken'),

]