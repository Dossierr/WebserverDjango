from django.urls import path
from .views import YourChatView  # Import your views from cases.views

app_name = 'cases'  # Optional, but it helps in namespacing URLs

urlpatterns = [
    path('your-case-view/', YourChatView, name='your-case-view'),
    path('your-other-view/', YourChatView, name='your-other-view'),
    # Add other URL patterns for your 'cases' app
]
