from django.shortcuts import render
from .forms import NameForm
import requests
from .models import SearchHistory
import json

# search 기능 기본 화면
def search_home(request):
    name = None
    api_response = None
    recent_searches = SearchHistory.objects.all().order_by('-search_date')[:5]  # 최신 검색어 5개 가져오기
    
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            api_response = search_cpe(name)
            
            # API 응답에서 cpe 항목만 추출
            if api_response is not None and 'cpes' in api_response:
                api_response = api_response['cpes']
            else:
                api_response = None

            #검색 기록 저장(결과가 없더라도 저장)
            save_search_history(name, api_response)

            #최근 검색어 리스트 업데이트
            recent_searches = SearchHistory.objects.all().order_by('-search_date')[:5]

    else:
        form = NameForm()

    # form, name, api_response를 템플릿으로 전달
    return render(request, 'search_home.html',
                  {'form': form, 'name': name, 
                   'api_response': api_response,
                   'recent_searches': recent_searches})


# 입력 제품명으로 cpe 검색
def search_cpe(name):
    api_url = 'https://cvedb.shodan.io/cpes'  
    params = {'product': name}  # API에 전달할 파라미터
    response = requests.get(api_url, params=params)
    
    # 응답 성공 여부 확인, JSON 응답 반환
    if response.status_code == 200:
        return response.json()
    else:
        return None

# 검색 기록을 데이터베이스에 저장하는 함수
def save_search_history(product_name, cpe_results):
    # cpe_results를 JSON 문자열로 변환해 저장
    cpe_results_json = json.dumps(cpe_results)
    
    # 검색 기록을 데이터베이스에 저장
    search_record = SearchHistory(product_name=product_name, cpe_result=cpe_results_json)
    search_record.save()

    #최대 5개까지 유지하도록 검색 기록 관리
    recent_count = SearchHistory.objects.count()
    if recent_count > 5:
        #가장 오래된 검색 기록 삭제
        oldest_record = SearchHistory.objects.order_by('search_date').first()
        if oldest_record:
            oldest_record.delete()

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