import humanize

from datetime import datetime

from django.views import View


from django.views.generic import FormView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin,UpdateView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q


from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger



from authapp.views import login
from authapp.forms import LoginForm

from .models import Project, Comment
from .forms import NewProjectForm, NewCommentForm, SelectCommentForm, UnSelectCommentForm
from django.http.response import HttpResponseForbidden


"""
VIEW FROM PROJECT APP
"""

def get_ranked_project_list():
    #get 20 most popular project desc (-)
    most_ranked_project = Project.objects.order_by('-mark')[:20]
    #use the title of the project like url parameter for the detail page.
    for project in most_ranked_project:
        project.url_detail = project.title.replace(" ","_")
        project.partial_username = project.user.username.split("@")[0]
    return most_ranked_project

def get_latest_project_list():
    #get 20 latest project desc (-)
    latest_project = Project.objects.order_by('date_last_modification')[:20]
    #use the title of the project like url parameter for the detail page.
    for project in latest_project:
        project.url_detail = project.title.replace(" ","_")
        project.partial_username = project.user.username.split("@")[0]
    return latest_project

def main(request):
    """
    Main Page
    """
    context = dict()
    context['ranked_project_list'] = get_ranked_project_list()
    context['latest_project_list'] = get_latest_project_list()
    return login(request,context)


@method_decorator(login_required, name='dispatch')
class ProjectNewView(FormView):
    """
    Create new project 
    """
    model = Project
    template_name = 'new_project.html'
    success_url = '/new-project/'
    form_class = NewProjectForm

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(ProjectNewView, self).get_form_kwargs(**kwargs)
        form_kwargs["user"] = self.request.user
        form_kwargs["mode"] = 'new' 
        return form_kwargs

    def get_context_data(self, **kwargs):
        context = super(ProjectNewView, self).get_context_data(**kwargs)
        context['page'] = 'new-project'
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'New project created successfully.')
        return super(ProjectNewView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProjectListView(ListView):
    """
    My projects 
    """
    model = Project
    template_name = 'my_projects.html'
    paginate_by = 15 

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs) 
        qs = super(ProjectListView, self).get_queryset()
        list_project = qs.filter(user=self.request.user)
        if len(list_project) == 0:
            context['object_list'] = list_project
            context['is_paginated'] = False
            return context

        #use the title of the project like url parameter for the detail page.
        for project in list_project:
            project.url_detail = project.title.replace(" ","_")
            project.partial_username = project.user.username.split("@")[0]
        
        paginator = Paginator(list_project, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            project_page = paginator.page(page)
        except PageNotAnInteger:
            project_page = paginator.page(1)
        except EmptyPage:
            project_page = paginator.page(paginator.num_pages)

        context['object_list'] = project_page
        context['page'] = 'my-projects'
        return context


class ProjectSearchResultsView(ListView):
    """
    Search Project 
    """
    model = Project
    template_name = 'search_results.html'
    paginate_by = 15 

    def find_projects(self,search_words,project_list):
        words_array = search_words.split()
        result = list()
        #search words in project titles
        for word in words_array:
            query_set = project_list.filter(title__contains=word)
            for e in query_set:
                result.append(e)    
        #search words in authors
        for word in words_array:
            query_set = project_list.filter(user__username__contains=word)
            for e in query_set:
                result.append(e)    
        #search worlds in tags
        for word in words_array:
            query_sey = project_list.filter(tags__tag__contains=word)   
            for e in query_set:
                result.append(e)
        #todo: remove duplicate project.
        return result

    def get_context_data(self, **kwargs):
        context = super(ProjectSearchResultsView, self).get_context_data(**kwargs) 
        project_list = super(ProjectSearchResultsView, self).get_queryset()
        search_words = self.request.GET.get('q')        
        result_project = self.find_projects(search_words,project_list)


        if len(result_project) == 0:
            context['object_list'] = result_project
            context['is_paginated'] = False
            context['display_login_form'] = True
            context['form'] = LoginForm()
            context['search_words'] = search_words
            return context

        #use the title of the project like url parameter for the detail page.
        for project in result_project:
            project.url_detail = project.title.replace(" ","_")
            project.partial_username = project.user.username.split("@")[0]
        
        paginator = Paginator(result_project, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            project_page = paginator.page(page)
        except PageNotAnInteger:
            project_page = paginator.page(1)
        except EmptyPage:
            project_page = paginator.page(paginator.num_pages)

        context['object_list'] = result_project
        context['display_login_form'] = True
        context['form'] = LoginForm()
        context['search_words'] = search_words 
        return context


class ProjectDetailView(FormMixin,DetailView):
    """
    Detail of Project 
    """
    model = Project
    template_name = 'detail_project.html'
    form_class = NewCommentForm

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(ProjectDetailView, self).get_form_kwargs(**kwargs)
        form_kwargs["user"] = self.request.user
        return form_kwargs

    def get_success_url(self):
        return reverse('detail-project', \
            kwargs={'project_title': self.object.title.replace(" ","_"),\
                    'user_id': self.object.user.id,\
                    'partial_username': self.object.user.username.split("@")[0]})

    #get the object with the title pass in the url
    def get_object(self):
        try:
            project_title = self.kwargs['project_title'].replace('_',' ')
            user_id = self.kwargs['user_id']
            partial_username = self.kwargs['partial_username']
            q = self.model.objects.filter(title__iexact=project_title).filter(user__username__icontains=partial_username)
            if(len(q) < 1):
                raise Http404
            return q[0]
        except Project.DoesNotExist:
            raise Http404
    

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        
        project = self.get_object()
        comment_list = Comment.objects.filter(project=project)
        #process day of the comment
        for comment in comment_list:
            comment.day = humanize.naturalday(comment.publication_date)

        context['comment_list'] = comment_list
        context['num_comments'] = len(comment_list)
        # display comment form if:
        #   * user is log in
        #   * the user dont have a comment in the project. 
        #   * the user is not the project owner
        if self.request.user.is_authenticated\
                and not self.is_second_comment(self.request.user,project)\
                and project.user.username != self.request.user.username:
            context['new_comment_form'] = self.get_form()
        
        project.url_detail = project.title.replace(" ","_")    
        context['project'] = project
        if project.user.username == self.request.user.username:
            context['display_edit_delete_button'] = True

        return context

    def is_second_comment(self,user,project):
        q = Comment.objects.filter(project=project).filter(user=user)
        return len(q) > 0

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Thanks for you comment.')
        return super(ProjectDetailView, self).form_valid(form)

@login_required
@require_http_methods(["POST"])
def selectComment(request,project_title,user_id):
    form = SelectCommentForm(project_title.replace('_',' '),user_id,request.POST)
    if form.is_valid():
        form.save()
    return redirect('edit-project', project_title=project_title, user_id=user_id)
    
@login_required
@require_http_methods(["POST"])
def unselectComment(request,project_title,user_id):
    form = UnSelectCommentForm(request.POST)
    if form.is_valid():
        form.save()
    return redirect('edit-project', project_title=project_title, user_id=user_id)


@method_decorator(login_required, name='dispatch')
class ProjectEditView(UpdateView):
    model = Project
    template_name = 'edit_project.html'
    success_url = '/my-projects/'
    form_class = NewProjectForm

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(ProjectEditView, self).get_form_kwargs(**kwargs)
        form_kwargs["user"] = self.request.user
        form_kwargs["mode"] = 'update'
        return form_kwargs


    #get the object with the title pass in the url
    def get_object(self):
        try:
            project_title = self.kwargs['project_title'].replace('_',' ')
            user_id = self.kwargs['user_id']
            q = self.model.objects.filter(title__iexact=project_title).filter(user__id=int(user_id))
            if(len(q) < 1):
                raise Http404
            return q[0]
        except Project.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(ProjectEditView, self).get_context_data(**kwargs)
        
        project = self.get_object()
        project.url_detail = project.title.replace(" ","_")
        comment_list = Comment.objects.filter(Q(project=project))
        selected_comment_list = comment_list.filter(Q(added_to_project=True)) 
        #process day of the comment
        for comment in comment_list:
            comment.day = humanize.naturalday(comment.publication_date)
        for comment in selected_comment_list:
            comment.day = humanize.naturalday(comment.publication_date)
            comment.form = UnSelectCommentForm( initial = {'idComment': comment.id})            

        context['project'] = project
        context['comment_list'] = comment_list
        context['num_comments'] = len(comment_list)
        context['select_comment_to_add_project'] = True
        
        selectedCommentForm = SelectCommentForm(project.title,project.user.id)
        if selectedCommentForm.has_comments:
            context['select_comment_form'] = selectedCommentForm 
        if len(selected_comment_list) > 0:
            context['selected_comment_list'] = selected_comment_list
        return context


    def get_initial(self):
        initial = super(ProjectEditView, self).get_initial()
        project = self.get_object()

        initial['title'] = project.title
        initial['summary'] = project.summary
        initial['advantages'] = project.advantages
        initial['investment'] = project.investment
        
        tags = project.tags.all();
        strTag = ''
        for tag in tags:
            strTag =  strTag + str(tag) + ','
        
        initial['tags'] = strTag[:-1]
        
        return initial