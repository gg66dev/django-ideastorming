from django import forms
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from django.db.models import Q

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
    
    def __init__(self, user, mode , *args, **kwargs):
        app_user = User.objects.get(username=user.username)
        self.app_user = app_user
        self.mode = mode
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
        if "." in title or "," in title or "_" in title:
            raise forms.ValidationError("Title can contain dots,commas or underscores")
        q = Project.objects.filter(user=self.app_user).filter(title=title)
        if len(q) > 0 and self.mode == 'new':
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
    score = forms.CharField(widget=forms.HiddenInput())

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


class SelectCommentForm(forms.Form):
    def __init__(self, project_title, user_id, *args, **kwargs):
        super(SelectCommentForm, self).__init__(*args, **kwargs)
        project = Project.objects.filter(user__id=user_id).filter(title=project_title);
        comments = Comment.objects.filter(Q(project=project) & Q(added_to_project=False))
        choices =  [ (str(o.id), str(o)) for o in comments ]
        self.fields['selected_comments'] = forms.MultipleChoiceField(
            choices = choices, 
            widget  = forms.CheckboxSelectMultiple,
        )
        self.valid_choices_id = [ str(o.id) for o in comments ]
        self.has_comments = len(comments) > 0

    def clean_selected_comment(self):
        selected_comments = self.cleaned_data['selected_comments']
        if not selected_comments:
            raise forms.ValidationError("This field is required.")
        for id in selected_comments:
            if id not in self.valid_choices_id:
                raise forms.ValidationError("invalid comment selected")
        return selected_comments
    
    def save(self):
        comment_selected_id = self.cleaned_data['selected_comments'] 
        for comment_id in comment_selected_id:
            comment = Comment.objects.get(id=comment_id)
            comment.added_to_project = True
            comment.save();



class UnSelectCommentForm(forms.Form):
    idComment = forms.IntegerField(widget=forms.HiddenInput())
    
    def save(self):
        comment_id = self.cleaned_data['idComment']
        comment = Comment.objects.get(id=comment_id)
        comment.added_to_project = False
        comment.save();




