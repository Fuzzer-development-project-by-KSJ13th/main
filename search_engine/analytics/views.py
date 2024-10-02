from django.shortcuts import render
from .models import Analytics
from django.http import JsonResponse
import requests
import json

def analytics_home(request):
    analytics = Analytics.objects
    if request.method == 'GET':
        cpe = request.GET.get('cpe')
    return render(request, 'analytics_search_cve.html', {'cpe':cpe})


def get_data(request):
    if request.method == 'GET':
        cpe = request.GET.get('cpe')
    response = requests.get(f"https://cvedb.shodan.io/cves?cpe23={cpe}")

    if response.status_code == 200:
        api_data = response.json()
        data = {'cve_id':[], 'cvss_value':[], 'epss':[]}
        for x in range(len(api_data['cves'])):
            cve_num = api_data['cves'][x]['cve_id']
            cvss_val = api_data['cves'][x]['cvss']
            epss_val = api_data['cves'][x]['epss']
            data['cve_id'].append(cve_num)
            data['cvss_value'].append(cvss_val)
            data['epss'].append(epss_val)
        
    return JsonResponse(data)