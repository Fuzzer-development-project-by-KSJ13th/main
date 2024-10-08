from django.shortcuts import render
from .forms import NameForm
import requests
from .models import SearchHistory
import json

# search 기능 기본 화면
def search_home(request):
    name = None
    user_name = request.user
    api_response = None
    recent_searches = SearchHistory.objects.filter(user=user_name).order_by('-search_date')[:5] 
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            search_option = form.cleaned_data['search_option']
            name = form.cleaned_data['name']

            if search_option == 'shodan':
                api_response = search_cpe(name)
                
                # API 응답에서 cpe 항목만 추출
                if api_response is not None and 'cpes' in api_response:
                    api_response = api_response['cpes']
                else:
                    api_response = None

            elif search_option == 'nvd':
                api_response = search_cpe_nvd(name)
                response_cpe_len = api_response['totalResults']
                cpe_names = []
                
                # API 응답에서 cpe 항목만 추출
                if api_response is not None and response_cpe_len > 0:
                    for product in api_response.get('products', []):
                        cpe = product.get('cpe', {})
                        cpe_name = cpe.get('cpeName')
                        if cpe_name:
                            cpe_names.append(cpe_name)
                    api_response = cpe_names
                else:
                    api_response = None
            
            save_search_history(user_name, name)
            recent_searches = SearchHistory.objects.filter(user=user_name).order_by('-search_date')[:5]

    else:
        form = NameForm()

    # form, name, api_response를 템플릿으로 전달
    return render(request, 'search_home.html',
                  {'form': form, 'name': name, 
                   'api_response': api_response,
                   'recent_searches': recent_searches})


# 입력 제품명으로 cpe 검색 at Shodan
def search_cpe(name):
    api_url = 'https://cvedb.shodan.io/cpes'  
    params = {'product': name}  # API에 전달할 파라미터
    response = requests.get(api_url, params=params)
    
    # 응답 성공 여부 확인, JSON 응답 반환
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
# 입력 제품명으로 cpe 검색 at NVD
def search_cpe_nvd(name):
    api_url = 'https://services.nvd.nist.gov/rest/json/cpes/2.0'
    params = {'keywordSearch' : name}
    response = requests.get(api_url, params=params)
    
    # 응답 성공 여부 확인, JSON 응답 반환
    if response.status_code == 200:
        return response.json()
    else:
        return None    

# 검색 기록을 데이터베이스에 저장하는 함수
def save_search_history(user, product_name):
    search_history = SearchHistory.objects.create(user=user, product_name=product_name)

    search_history_count = SearchHistory.objects.filter(user=user).count()
    if search_history_count > 5:
        oldest_searches = SearchHistory.objects.filter(user=user).order_by('search_date')[:search_history_count - 5]
        for search in oldest_searches:
            search.delete()



    return search_history

def get_cve_form_cpe(request, cpe):
    api_url = 'https://cvedb.shodan.io/cves'
    params = {'cpe23' : cpe}
    response = requests.get(api_url, params=params)
    
    # 응답 성공 여부 확인, JSON 응답 반환
    if response.status_code == 200:
        cve_list = response.json()
    else:      # 에러 처리
        error_message = response.text  
        cve_list = {
            'error': f"Error {response.status_code}: {error_message}"
        }
        print(f"API Error: {error_message}")  

    return render(request, 'cve_list.html', {'cve_list': cve_list})