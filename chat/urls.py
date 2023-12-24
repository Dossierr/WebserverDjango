from django.urls import path
from .views import chat_history_view, query_endpoint  # Import your views from chat.views

app_name = 'chat'  # Optional, but it helps in namespacing URLs

urlpatterns = [
    path('history/<str:case_id>/', chat_history_view, name='chat-history'),
    path('query', query_endpoint, name='query-endpoint'),]
