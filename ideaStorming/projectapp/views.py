import humanize

from datetime import datetime

#from django.views.generic.edit import CreateView
from django.views.generic import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages
from django.urls import reverse

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger



from authapp.views import login
from authapp.forms import LoginForm

from .models import Project, Comment
from .forms import NewProjectForm, NewCommentForm
from django.http.response import HttpResponseForbidden


"""
VIEW FROM PROJECT APP
"""

def index(request):
    """
    Main Page
    """
    context = dict()
    #get 20 most popular project desc (-)
    most_ranked_project = Project.objects.order_by('-mark')[:20] 
    context['ranked_project_list'] = most_ranked_project
    #get 20 latest project desc (-)
    latest_project = Project.objects.order_by('date_last_modification')[:20]
    context['latest_project_list'] = latest_project

    return login(request,context)


@method_decorator(login_required, name='dispatch')
class ProjectNewView(FormView):
    """
    Create new project view
    """
    model = Project
    template_name = 'new_project.html'
    success_url = '/new-project/'
    form_class = NewProjectForm

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(ProjectNewView, self).get_form_kwargs(**kwargs)
        form_kwargs["user"] = self.request.user
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
    My projects View
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
            project.url_detail = project.title.replace(" ", "_")
        
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
    Search Project View
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
            project.url_detail = project.title.replace(" ", "_")
        
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
    Detail of Project view
    """
    model = Project
    template_name = 'detail_project.html'
    form_class = NewCommentForm

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(ProjectDetailView, self).get_form_kwargs(**kwargs)
        form_kwargs["user"] = self.request.user
        return form_kwargs

    def get_success_url(self):
        return reverse('detail-project', kwargs={'project_title': self.object.title.replace(" ", "_")})

    #get the object with the title pass in the url
    def get_object(self):
        title = self.kwargs['project_title'].replace("_", " ")
        try:
            #problem: Enter to detail project from search or top 20 columns.
            #project = self.model.objects.filter(user=self.request.user).get(title__iexact=title) 
            project = self.model.objects.get(title__iexact=title)
        except Project.DoesNotExist:
            raise Http404
        return project

    
    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['page'] = 'my-projects'

        #comments
        title = self.kwargs['project_title'].replace("_", " ")
        #project = self.model.objects.filter(user=self.request.user).get(title__iexact=title)
        project = self.model.objects.get(title__iexact=title)
        comment_list = Comment.objects.filter(project=project)
        #process day of the comment
        for comment in comment_list:
            comment.day = humanize.naturalday(comment.publication_date)

        context['comment_list'] = comment_list
        context['num_comments'] = len(comment_list)
        # display form if:
        #   * user is log in
        #   * the user dont have a comment in the project. 
        #   * the user is not the project owner
        if self.request.user.is_authenticated\
                and not self.is_second_comment(self.request.user,project)\
                and project.user.username != self.request.user.username:
            context['new_comment_form'] = self.get_form()
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