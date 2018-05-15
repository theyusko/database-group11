from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

	url(r'^id/player(?P<id>\d+)$', views.player, name='player'),
	url(r'^id/auth/player(?P<id>\d+)$', views.playerauth, name='player'),
	url(r'^form_player', views.form_player, name="form_player"),
	url(r'^player_register', views.player_register, name="player_register"),

	url(r'^id/agent(?P<id>\d+)$', views.agent, name = "agent"),
	url(r'^id/auth/agent(?P<id>\d+)$', views.agentauth, name = "agent"),
	url(r'^form_agent', views.form_agent, name="form_agent"),
	url(r'^agent_register', views.agent_register, name="agent_register"),

	url(r'^id/president(?P<id>\d+)$', views.president, name = "president"),
	url(r'^id/auth/president(?P<id>\d+)$', views.presidentauth, name = "presidentauth"),
	url(r'^form_president', views.form_president, name="form_president"),
	url(r'^president_register', views.president_register, name="president_register"),

	url(r'^id/coach(?P<id>\d+)$', views.coach, name = "coach"),
	url(r'^id/auth/coach(?P<id>\d+)$', views.coachauth, name = "coach"),
	url(r'^form_coach', views.form_coach, name="form_coach"),
	url(r'^coach_register', views.coach_register, name="coach_register"),


	url(r'^leagueSelection/(?P<string>[\w\-]+)$', views.leagues_info, name="leagueselectedLeague"),
    url(r'^leagueSelection', views.league, name="leagueSelection"),
	]