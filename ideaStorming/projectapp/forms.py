from django import forms
from django.forms import ModelForm
from django.utils.safestring import mark_safe

from authapp.models import User
from .models import Project, Tag, Comment

class TagListWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        output = []
        output.append(u'<div id="tag_container" class="input textarea clearfix custom stackoverflow"></div>')
        output.append(super(TagListWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))



class NewProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ( 'title', 'summary', 'advantages','investment','tags' )
    class Media:
        js = {'js/taglist-widget.js'}

    
    tags = forms.CharField(widget=TagListWidget())
    
    def __init__(self, user, *args, **kwargs):
        app_user = User.objects.get(username=user.username)
        self.app_user = app_user
        super(NewProjectForm, self).__init__(*args, **kwargs)
    
    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if not tags:
            raise forms.ValidationError("This field is required.")
        return tags

    def clean_title(self):
        #check that title dont contain dots or commas.
        #check that user hasnt other project with the same name.
        title = self.cleaned_data['title']
        if "." in title or "," in title:
            raise forms.ValidationError("Title can contain dots or commas")
        q = Project.objects.filter(user=self.app_user).filter(title=title)
        if len(q) > 0:
            raise forms.ValidationError("You already have a project with this title, please change the title.")
        return title

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



class NewCommentForm(ModelForm):
    project_title = forms.CharField(required=True, max_length= 200)

    class Meta:
        model = Comment
        fields = ( 'project_title', 'comment', 'score')


    def __init__(self, user, *args, **kwargs):
        try:
            app_user = User.objects.get(username=user.username)
            self.app_user = app_user
        except:
            self.app_user = None
        super(NewCommentForm, self).__init__(*args, **kwargs)
    
    def clean_project_title(self):
        project_title = self.cleaned_data['project_title']
        if not project_title:
            raise forms.ValidationError("This field is required.")
        return project_title

    def save(self, commit=True):
        """
        desc: get project by title and set value in comment instance.
        """
        comment_instance = super(NewCommentForm, self).save(commit=False)
        project_title = self.cleaned_data['project_title']
        project = Project.objects.get(title=project_title)
        comment_instance.project = project 
        comment_instance.user = self.app_user
        if commit:
            comment_instance.save()
        return comment_instance
