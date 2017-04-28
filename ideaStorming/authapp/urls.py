from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.UserRegister.as_view(), name='register'),
    url(r'^logout/$', views.logout, name='logout'),
]
