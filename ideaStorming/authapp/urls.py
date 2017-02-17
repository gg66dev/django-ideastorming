from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.UserRegister.as_view(), name='register'),
    #url(r'^login/$', views.login), #login same view that index
    url(r'^logout/$', views.logout, name='logout'),
]
