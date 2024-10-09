from django.shortcuts import render
from api_search.models import SearchHistory
from django.db.models import Count
from django.utils import timezone

def home(request):
    return render(request, 'home.html', {'user': request.user})

def charts(request):
    product_counts = SearchHistory.objects.values('product_name').annotate(search_count=Count('product_name')).order_by('-search_count')

    # 리스트로 변환하여 템플릿에 전달
    product_names = [item['product_name'] for item in product_counts]
    search_counts = [item['search_count'] for item in product_counts]

    # 가장 최근 검색 날짜
    latest_search_date = SearchHistory.objects.latest('search_date').search_date

    context = {
        'product_names': product_names,
        'search_counts': search_counts,
        'latest_search_date': latest_search_date
    }
    
    return render(request, 'charts.html', context)