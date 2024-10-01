from django.shortcuts import render
from .forms import NameForm

def search_home(request):
    name = None
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            # 폼이 유효하면, 사용자가 입력한 데이터를 가져옵니다.
            name = form.cleaned_data['name']
    else:
        form = NameForm()

    # 폼과 이름을 모두 템플릿으로 전달
    return render(request, 'search_home.html', {'form': form, 'name': name})
