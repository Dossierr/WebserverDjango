from django.urls import path, include
from .views import product_page, payment_successful, payment_cancelled, stripe_webhook
# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('product_page', product_page, name='product_page'),
    path('payment_successful', payment_successful, name='payment_succesful'),
    path('payment_cancelled', payment_cancelled, name='payment_cancelled'),
    path('stripe-webhook', stripe_webhook, name='stripe_webhook')
]
