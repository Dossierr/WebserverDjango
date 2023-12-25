
# Create your views here.
from django.shortcuts import render

def profile_view(request):
    return render(request, 'profile.html', {'title': 'Profile'})

def dashboard_view(request):
    return render(request, 'dashboard.html', {'title': 'Dashboard'})

def settings_view(request):
    return render(request, 'settings.html', {'title': 'Settings'})