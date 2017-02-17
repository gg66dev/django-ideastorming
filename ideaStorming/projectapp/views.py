from django.shortcuts import render, redirect
from authapp.views import login

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        fullname = request.user.first_name + " " + request.user.last_name
        return render(request, 'index.html', { 'fullname': fullname})
    else:
        return login(request)