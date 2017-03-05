#from django.views.generic.edit import CreateView
from django.views.generic import FormView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

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
    return login(request)


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
        return super(ProjectNewView, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class ProjectListView(ListView):
    model = Project
    template_name = 'my_projects.html'
    paginate_by = 15 

    #def get_queryset(self):
    #    qs = super(ProjectListView, self).get_queryset()
    #    return qs.filter(user=self.request.user)
       

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs) 
        qs = super(ProjectListView, self).get_queryset()
        list_exam = qs.filter(user=self.request.user)
        paginator = Paginator(list_exam, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        context['object_list'] = file_exams
        return context