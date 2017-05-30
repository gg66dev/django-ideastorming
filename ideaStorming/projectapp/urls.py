from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^new-project/$', views.ProjectNewView.as_view(), name='new-project'),
    url(r'^my-projects/$', views.ProjectListView.as_view(), name='my-projects'),
    url(r'^detail-project/(?P<project_title>[\w.@+-]+)/(?P<user_id>\d+)/(?P<partial_username>[\w]+)/$', 
        views.ProjectDetailView.as_view(), name='detail-project'),
    url(r'^delete-project/(?P<project_title>[\w.@+-]+)/(?P<user_id>\d+)/$', 
        views.ProjectDeleteView.as_view(), name='delete-project'),
    url(r'^edit-project/(?P<project_title>[\w.@+-]+)/(?P<user_id>\d+)/$', 
        views.ProjectEditView.as_view(), name='edit-project'),
    url(r'^search/$',views.ProjectSearchResultsView.as_view(), name='search'),
]