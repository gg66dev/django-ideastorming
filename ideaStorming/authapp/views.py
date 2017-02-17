from django.shortcuts import render,redirect
from django.views.generic import FormView
from django.contrib.auth import authenticate, login as django_login, logout as django_logout

from .models import User
from .forms import UserForm, LoginForm


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            username =  form.cleaned_data.get('email')
            user = authenticate(username=username, password=password)
            django_login(request,user)
            #use user info to display in the view
            fullname = user.first_name + " " + user.last_name
            return render(request, 'index.html', { 'fullname': fullname})
    else:
        form = LoginForm()
    return render(request, 'index.html', {'form': form , 'display_login_form':True})
    

def logout(request):
    django_logout(request)
    return redirect('/') #redirect to index



# FormView para registrar usuarios
class UserRegister(FormView):
    model = User
    template_name = 'user_register.html'
    form_class = UserForm
    success_url = '/register/'

    def form_valid(self, form):
        form.save()
        return super(UserRegister, self).form_valid(form)