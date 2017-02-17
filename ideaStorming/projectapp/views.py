from django.shortcuts import render, redirect
from authapp.views import login

# Create your views here.

def index(request):
    return login(request)
    