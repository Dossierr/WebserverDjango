from django.urls import path
from .views import landing_page_view

urlpatterns = [
    path('', landing_page_view, name='landing_page'),
    path('login', landing_page_view, name='login'),
    path('register', landing_page_view, name='signup'),
    path('logout', landing_page_view, name='logout'),
    
    # Add other paths as needed
]