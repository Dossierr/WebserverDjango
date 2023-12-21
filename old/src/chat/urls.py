from django.urls import path
from .views import chat_page_view

urlpatterns = [
    path('', chat_page_view, name='dashboard'),

    
]