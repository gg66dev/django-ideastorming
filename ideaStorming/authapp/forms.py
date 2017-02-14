from django import forms
from django.forms import ModelForm
from authapp.models import User

class UserForm(ModelForm):
    confirm_password = forms.CharField()
    class Meta:
        model = User
        fields = [ 'first_name', 'last_name' , 'email' ,'company', 'country', 'password', 'confirm_password']
        
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