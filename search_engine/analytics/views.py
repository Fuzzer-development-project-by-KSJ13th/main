from django.shortcuts import render
from .models import Analytics
from django.http import JsonResponse
import requests


def analytics_home(request):
    analytics = Analytics.objects
    return render(request, 'analytics_home.html', {'analytics':analytics})


def get_data(request):
    response = requests.get('https://cvedb.shodan.io/cves?product=flask&count=false&is_kev=false&sort_by_epss=false&skip=0&limit=1000')
    
    if response.status_code == 200:
        api_data = response.json()

        data = {'cve_id':[], 'cvss_value':[]}

        for i in range(len(api_data['cves'])):
            cve_num = api_data['cves'][i]['cve_id']
            cvss_val = api_data['cves'][i]['cvss']
            
            data['cve_id'].append(cve_num)
            data['cvss_value'].append(cvss_val)
        print(data)

    return JsonResponse(data)
