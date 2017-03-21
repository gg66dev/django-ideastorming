#from django.views.generic.edit import CreateView
from django.views.generic import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger


from authapp.views import login

from .models import Project
from .forms import NewProjectForm


"""
VIEW FROM PROJECT APP
"""

def index(request):
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



@method_decorator(login_required, name='dispatch')
class ProjectDetailView(DetailView):
    model = Project
    template_name = 'detail_project.html'
    
    #get the object with the title pass in the url
    def get_object(self):
        title = self.kwargs['project_title'].replace("_", " ")
        try:
            project = self.model.objects.filter(user=self.request.user).get(title__iexact=title) 
        except Project.DoesNotExist:
            raise Http404
        return project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['page'] = 'my-projects'
        return context