from django.db import models
from django.utils import timezone

class Search(models.Model):
    keyword = models.TextField()

class SearchHistory(models.Model):
    product_name = models.CharField(max_length=255)  # 검색한 제품명
    cpe_result = models.TextField()  # CPE 검색 결과 (JSON 형태로 저장 가능)
    search_date = models.DateTimeField(default=timezone.now)  # 검색한 시간
    username = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.product_name
