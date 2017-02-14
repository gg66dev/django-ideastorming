from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate

from authapp.models import User


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise forms.ValidationError("This field is required.")
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if not password:
            raise forms.ValidationError("This field is required.")
        return password
    
    def clean(self):
        #check authentication and do login also.
        password = self.cleaned_data.get('password')
        username =  self.cleaned_data.get('email')
        user = authenticate(username=username, password=password)
        if user is None:    
            raise forms.ValidationError("You entered an incorrect username or password")
        return self.cleaned_data                            

class UserForm(ModelForm):
    confirm_password = forms.CharField()
    class Meta:
        model = User
        fields = [ 'first_name', 'last_name' , 'email' ,'company', 'country', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput()
        }

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise forms.ValidationError("This field is required.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name:
            raise forms.ValidationError("This field is required.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise forms.ValidationError("This field is required.")
        return email

    def clean(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords dont match.")
        return self.cleaned_data

    #use email like username
    def save(self, commit=True):
        instance = super(UserForm, self).save(commit=False)
        instance.username = self.cleaned_data['email']
        password = self.cleaned_data['password'] 
        instance.set_password(password)
        if commit:
            instance.save()
        return instance