from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^new-project/$', views.ProjectNewView.as_view(), name='new-project'),
    url(r'^my-projects/$', views.ProjectListView.as_view(), name='my-projects'),
    url(r'^detail-project/(?P<project_title>[\w\-]+)/$', views.ProjectDetailView.as_view(), name='detail-project'),
    url(r'^search/$',views.ProjectSearchResultsView.as_view(), name='search'),
]