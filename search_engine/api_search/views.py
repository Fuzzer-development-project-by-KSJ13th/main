from django.shortcuts import render
from .models import Search

def search_home(request):
    searches = Search.objects
    return render(request, 'search_home.html', {'searches':searches})