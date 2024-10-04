from django.shortcuts import render
from .models import Analytics
import requests
import json

def analytics_home(request):
    analytics = Analytics.objects
    return render(request, 'analytics_home.html', {'analytics':analytics})


def get_cve_id(request):
    if request.method == 'GET':
        cpe = request.GET['cpe']
    
    #cpe = 'cpe:2.3:a:libpng:libpng:0.8'
    response = requests.get(f"https://cvedb.shodan.io/cves?cpe23={cpe}").json()

    cves = response['cves']
    '''
    for cve in cves:
        print(f"CVE ID: {cve['cve_id']}")
        print(f"Summary: {cve['summary']}")
        print(f"CVSS v2: {cve['cvss_v2']}")
        print(f"CVSS v3: {cve['cvss_v3']}")
        print(f"EPSS: {cve['epss']}")
        print(f"Published Time: {cve['published_time']}")
        print("References:")
        for ref in cve['references']:
            print(ref)
        print("="*40)
    '''
    
    return render(request, 'analytics_search_cve.html', {'list':response})
   #return render(request, 'analytics_search_cve.html', {'cpe':cpe,'cves':value})