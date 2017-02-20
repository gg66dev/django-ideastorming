from django.db import models

from authapp.models import User

class Tag(models.Model):
    tag = models.CharField(max_length=30)
   

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
    date_creation =  models.DateTimeField(auto_now_add=True, blank=True) 
    date_last_modification =  models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    score  = models.IntegerField()
    comment = models.CharField(max_length=300)