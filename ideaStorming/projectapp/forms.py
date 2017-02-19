from django import forms
from django.forms import ModelForm

from .models import Project

class NewProjectForm(ModelForm):
    tags = forms.CharField(required=True, max_length= 200)
    
    class Meta:
        model = Project
        fields = ( 'title', 'summary', 'advantages','investment','tags' )


