from django.urls import path
from .views import profile_view, dashboard_view, settings_view

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('', dashboard_view, name='dashboard'),
    path('settings/', settings_view, name='settings'),
]
