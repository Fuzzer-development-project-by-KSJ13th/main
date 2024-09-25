from django.shortcuts import render
from .models import Analytics

def analytics_home(request):
    analytics = Analytics.objects
    return render(request, 'analytics_home.html', {'analytics':analytics})