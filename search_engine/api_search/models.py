from django.db import models

class Search(models.Model):
    keyword = models.TextField()
