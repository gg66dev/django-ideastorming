from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new-project/$', views.ProjectNewView.as_view(), name='new-project'),
    url(r'^my-projects/$', views.ProjectListView.as_view(), name='my-projects'),
    url(r'^my-projects/(?P<project_title>[\w\-]+)/$', views.ProjectDetailView.as_view(), name='detail-project'),
]