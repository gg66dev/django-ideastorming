from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new-project/$', views.ProjectNewView.as_view(), name='new-project'),
    url(r'^my-projects/$', views.ProjectListView.as_view(), name='my-projects')
]