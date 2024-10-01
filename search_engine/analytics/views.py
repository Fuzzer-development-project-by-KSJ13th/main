from django.shortcuts import render
from .models import Analytics
from django.http import JsonResponse
import requests
import json

def analytics_home(request):
    analytics = Analytics.objects
    return render(request, 'analytics_search_cve.html', {'analytics':analytics})


def get_data(request):
    '''
    if request.method == 'GET':
        cpe = request.GET['cpe']
    '''
    #cpe = 'cpe:2.3:a:libpng:libpng:0.8'
    #response = requests.get(f"https://cvedb.shodan.io/cves?cpe23={cpe}")
    response = requests.get(f"https://cvedb.shodan.io/cves?cpe23=cpe:2.3:a:libpng:libpng:0.8")

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
   #return render(request, 'analytics_search_cve.html', {'cpe':cpe,'cves':value})