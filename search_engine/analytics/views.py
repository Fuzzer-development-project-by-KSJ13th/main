#from django.core.paginator import Paginator
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
    '''
    if request.method == 'GET':
        cpe = request.GET['cpe']
    '''

    #cpe = 'cpe:2.3:a:libpng:libpng:0.8'
    #response = requests.get(f"https://cvedb.shodan.io/cves?cpe23={cpe}")
    #response = requests.get(f"https://cvedb.shodan.io/cves?cpe23=cpe:2.3:a:libpng:libpng:0.8")
    #response = requests.get(f"https://cvedb.shodan.io/cves")
    if request.method == 'GET':
        cpe = request.GET.get('cpe')
    response = requests.get(f"https://cvedb.shodan.io/cves?cpe23={cpe}")

    if response.status_code == 200:
        api_data = response.json()
        data = {'cve_id':[], 'cvss_value':[], 'epss':[], 'summary':[], 'references':[], 'published_time':[], 'cvss_v2':[], 'cvss_v3':[]}
        for x in range(len(api_data['cves'])):
            cve_num = api_data['cves'][x]['cve_id']
            cvss_val = api_data['cves'][x]['cvss']
            epss_val = api_data['cves'][x]['epss']
            cve_summary = api_data['cves'][x]['summary']
            references = api_data['cves'][x]['references']
            cvss_v2 = api_data['cves'][x]['cvss_v2']
            cvss_v3 = api_data['cves'][x]['cvss_v3']
            published_time = api_data['cves'][x]['published_time']
            

            data['cve_id'].append(cve_num)
            data['cvss_value'].append(cvss_val)
            data['epss'].append(epss_val)
            data['summary'].append(cve_summary)
            data['references'].append(references)
            data['published_time'].append(published_time)
            data['cvss_v2'].append(cvss_v2)
            data['cvss_v3'].append(cvss_v3)
        
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
                'references': cve_data.get('references', []),
                'published_time':cve_data['published_time'],
                'cvss_v2':cve_data['cvss_v2'],
                'cvss_v3':cve_data['cvss_v3']
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'CVE not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

