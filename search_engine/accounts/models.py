from django.db import models

# Create your models here.

# models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    job = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
