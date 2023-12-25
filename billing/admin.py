from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserPayment

class UserPaymentAdmin(admin.ModelAdmin):
    list_display = ('app_user', 'payment_bool', 'stripe_checkout_id')
    list_filter = ('payment_bool',)
    search_fields = ('app_user__username', 'stripe_checkout_id')

admin.site.register(UserPayment, UserPaymentAdmin)