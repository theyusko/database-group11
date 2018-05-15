from django.contrib import admin
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^authenticated', views.authenticatedMainPage, name="authenticatedMainPage"),
]