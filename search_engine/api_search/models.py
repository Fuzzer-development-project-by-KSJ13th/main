from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Search(models.Model):
    keyword = models.TextField()

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)  # 검색한 제품명
    # cpe_result = models.TextField()  # CPE 검색 결과 (JSON 형태로 저장 가능)
    search_date = models.DateTimeField(default=timezone.now)  # 검색한 시간

    def __str__(self):
        return f'{self.user.username}:{self.product_name}'