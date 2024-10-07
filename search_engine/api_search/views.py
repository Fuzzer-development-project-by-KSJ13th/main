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
    
    # 사용자 인증 여부 확인 및 username 저장
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    
    #print(username)

    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            search_term = name.lower()   #소문자로 변환하여 검색
            api_response = search_cpe(search_term)
            
            # API 응답에서 cpe 항목만 추출
            if api_response is not None and 'cpes' in api_response:
                api_response = api_response['cpes']
            else:
                api_response = None

            # 검색 기록 저장(결과가 없더라도 저장), username도 함께 저장
            save_search_history(name, api_response, username)

            # 최근 검색어 리스트 업데이트
            recent_searches = SearchHistory.objects.all().order_by('-search_date')[:5]

    else:
        form = NameForm()

    # form, name, api_response, recent_searches, username을 템플릿으로 전달
    return render(request, 'search_home.html',
                  {'form': form, 'name': name, 
                   'api_response': api_response,
                   'recent_searches': recent_searches,
                   'username': username})


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
def save_search_history(product_name, cpe_results, username):
    # cpe_results를 JSON 문자열로 변환해 저장
    cpe_results_json = json.dumps(cpe_results)
    
    # 검색 기록을 데이터베이스에 저장, username도 함께 저장
    search_record = SearchHistory(
        product_name=product_name, 
        cpe_result=cpe_results_json,
        username=username  # username을 저장
    )
    search_record.save()


def get_cve_form_cpe(request, cpe):
    api_url = 'https://cvedb.shodan.io/cves'
    params = {'cpe23': cpe}
    response = requests.get(api_url, params=params)
    
    # 응답 성공 여부 확인, JSON 응답 반환
    if response.status_code == 200:
        cve_list = response.json()
    else:  # 에러 처리
        error_message = response.text  
        cve_list = {
            'error': f"Error {response.status_code}: {error_message}"
        }
        print(f"API Error: {error_message}")

    return render(request, 'cve_list.html', {'cve_list': cve_list})
