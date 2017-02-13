from django import forms
from django.forms import ModelForm
from authapp.models import User

class UserForm(ModelForm):
    confirm_password = forms.CharField()
    class Meta:
        model = User
        fields = [ 'first_name', 'last_name' , 'email' ,'company', 'country', 'password', 'confirm_password']
        
