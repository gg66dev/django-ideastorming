
from django.contrib.auth.models import User as Django_user
from django.db import models

# Create your models here.


class User(Django_user):
    country = models.CharField(max_length=50)
    company = models.CharField(max_length=50)