from django import forms
from django.forms import ModelForm

from authapp.models import User
from .models import Project, Tag

class NewProjectForm(ModelForm):
    tags = forms.CharField(required=False, max_length= 200)
    
    class Meta:
        model = Project
        fields = ( 'title', 'summary', 'advantages','investment','tags' )

    def __init__(self, user, *args, **kwargs):
        app_user = User.objects.get(username=user.username)
        self.app_user = app_user
        super(NewProjectForm, self).__init__(*args, **kwargs)
    
    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if not tags:
            raise forms.ValidationError("This field is required.")
        return tags


    def save(self, commit=True):
        """
        tags - would parse de values of field tag from form, create 
            the object (or find if the tag exist) and then link to the project
        """
        project_instance = super(NewProjectForm, self).save(commit=False)
        project_instance.user = self.app_user
        if commit:
            #save objects
            project_instance.save()
        
        #parse tags and create objects
        tags_unparsed = self.cleaned_data['tags']
        tags = [x.strip() for x in tags_unparsed.split(',')]
        for tag_name in tags:
            tag_instance = Tag(tag=tag_name)
            tag_instance.save()
            project_instance.tags.add(tag_instance)        
        
        return project_instance