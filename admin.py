from django.contrib import admin

# Register your models here.
from .models import SearchHistory

# SearchHistory 모델을 관리자 페이지에 등록
admin.site.register(SearchHistory)
