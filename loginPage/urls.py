from django.contrib import admin
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^registerPage', views.registerPage, name="registerPage"),
    url(r'^requestLogin', views.requestLogin, name="requestLogin"),
]