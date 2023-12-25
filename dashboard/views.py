
# Create your views here.
from django.shortcuts import render

from django.shortcuts import render
from cases.models import Case, File

def dashboard_view(request):
    # Assuming you have a user associated with the request, you can replace 'user' with your actual user variable
    user = request.user
    
    # Fetch all cases for the logged-in user
    cases = Case.objects.filter(user=user)
    
    # Fetch all files related to the cases for the logged-in user
    files = File.objects.filter(case__user=user)
    
    context = {
        'title': 'Dashboard',
        'cases': cases,
        'files': files,
    }
    
    return render(request, 'dashboard.html', context)

def settings_view(request):
    return render(request, 'settings.html', {'title': 'Settings'})


def profile_view(request):
    return render(request, 'profile.html', {'title': 'Profile'})