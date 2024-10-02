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
    #response = requests.get(f"https://cvedb.shodan.io/cves")

    if response.status_code == 200:
        api_data = response.json()
        data = {'cve_id':[], 'cvss_value':[], 'epss':[], 'summary':[]}
        for x in range(len(api_data['cves'])):
            cve_num = api_data['cves'][x]['cve_id']
            cvss_val = api_data['cves'][x]['cvss']
            epss_val = api_data['cves'][x]['epss']
            cve_summary = api_data['cves'][x]['summary']
            

            data['cve_id'].append(cve_num)
            data['cvss_value'].append(cvss_val)
            data['epss'].append(epss_val)
            data['summary'].append(cve_summary)
            
        
    return JsonResponse(data)
   #return render(request, 'analytics_search_cve.html', {'cpe':cpe,'cves':value})

def cve_info(request, cve_id):
    try:
        response = requests.get(f"https://cvedb.shodan.io/cve/{cve_id}")
        if response.status_code == 200:
            cve_data = response.json()
            data = {
                'cve_id': cve_data['cve_id'],
                'summary': cve_data['summary'],
                'cvss_score': cve_data['cvss'],
                'epss': cve_data['epss'],
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'CVE not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

