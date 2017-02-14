from django.shortcuts import render
from django.views.generic import FormView

from .models import User
from .forms import UserForm

"""
ref:
https://docs.djangoproject.com/en/1.10/topics/auth/default/#how-to-log-a-user-in
https://docs.djangoproject.com/en/1.10/topics/auth/default/#how-to-log-a-user-out
http://test-driven-django-development.readthedocs.io/en/latest/05-forms.html
"""


# FormView para registrar usuarios
class UserRegister(FormView):
    model = User
    template_name = 'user_register.html'
    form_class = UserForm
    success_url = '/register/'