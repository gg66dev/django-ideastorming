from django.shortcuts import render,redirect
from django.views.generic import FormView
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from .models import User
from .forms import UserForm, LoginForm


"""
VIEW FROM AUTH APP
"""

def login(request,context):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            username =  form.cleaned_data.get('email')
            user = authenticate(username=username, password=password)
            django_login(request,user)
            #use user info to display in the view
            context['page'] = 'home'
            return render(request, 'index.html', context)
    else:
        form = LoginForm()

    context['form'] = form
    context['display_login_form'] = True
    context['page'] = 'home'
    return render(request, 'index.html', context)

def logout(request):
    django_logout(request)
    form = LoginForm()
    return redirect('index')


class UserRegister(FormView):
    model = User
    template_name = 'new_user.html'
    form_class = UserForm
    success_url = '/register/'
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'New user created successfully.')
        return super(UserRegister, self).form_valid(form)
    
   
   