from django.shortcuts import render
from .forms import NameForm
import requests

# search 기능 기본 화면
def search_home(request):
    name = None
    api_response = None
    cpes = []
    
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            api_response = search_cpe(name)

    else:
        form = NameForm()

    # form, name, api_response를 템플릿으로 전달
    return render(request, 'search_home.html', {'form': form, 'name': name, 'api_response': api_response['cpes']})


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