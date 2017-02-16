
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles import views

urlpatterns = [
    url(r'^',include('authapp.urls')),
    url(r'^',include('projectapp.urls')),
    url(r'^admin/', admin.site.urls),
]
