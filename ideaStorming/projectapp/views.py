from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required



from authapp.views import login

from .models import Project
from .forms import NewProjectForm


"""
VIEW FROM PROJECT APP
"""

def index(request):
    return login(request)


@method_decorator(login_required, name='dispatch')
class NewProject(CreateView):
    model = Project
    template_name = 'new_project.html'
    success_url = '/new-project/'
    form_class = NewProjectForm


  
    def get_context_data(self, **kwargs):
        context = super(NewProject, self).get_context_data(**kwargs)
        context['page'] = 'new-project'
        return context

    