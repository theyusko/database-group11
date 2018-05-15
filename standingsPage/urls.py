from django.contrib import admin
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.league, name='league'),
    url(r'^leagueSelection/(?P<league>[\D+/]+)$', views.league_standings, name="leagueselectedLeague"),
]