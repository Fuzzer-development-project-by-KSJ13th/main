from django.shortcuts import render
from .models import Analytics
from django.http import JsonResponse
import requests


def analytics_home(request):
    analytics = Analytics.objects
    return render(request, 'analytics_home.html', {'analytics':analytics})


def get_data(request):
    response = requests.get('https://cvedb.shodan.io/cves?cpe23=cpe%3A2.3%3Aa%3Apalletsprojects%3Aflask%3A1.1.4&count=false&is_kev=false&sort_by_epss=false&skip=0&limit=1000')
    
    if response.status_code == 200:
        api_data = response.json()
        cve_num = api_data['cves'][0]['cve_id']
        cvss_val = api_data['cves'][0]['cvss']
        data = {
            'cve_id' : [cve_num],
            'cvss_value' : [cvss_val]

        }
        
    return JsonResponse(data)
