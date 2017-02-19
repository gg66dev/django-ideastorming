from django.db import models

from authapp.models import User

class Project(models.Model):
    INVESTMENT_OPTIONS = (
        ('< $100 USD', '< $100 USD'),
        ('$100 - $300 USD', '$100 - $300 USD'),
        ('$301 - $500 USD', '$301 - $500 USD'),
        ('$501 - $800 USD', '$501 - $800 USD'),
        ('$801 - $1000 USD', '$801 - $1000 USD'),
        ('> $1000 USD', '> $1000 USD'),
    )
    
    title = models.CharField(max_length=30) 
    summary = models.TextField()
    advantages = models.TextField()
    investment = models.CharField(max_length=100, choices=INVESTMENT_OPTIONS)
    date_creation =  models.DateField() 
    date_last_modification =  models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Tag(models.Model):
    tag = models.CharField(max_length=30)
    project = models.ManyToManyField(Project)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    score  = models.IntegerField()
    comment = models.CharField(max_length=300)