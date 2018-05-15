from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection,transaction
import datetime

#In registration, check before inserting an agent whether the target player has an agent & similarly others

# Create your views here.
def index(request):
	cursor = connection.cursor()
	cursor.execute("""select account_id, name, surname, nationality, age, kit_no, pref_foot, 
		prev_transfer_fee, recovery_date, suspend_date, belong_to_team_name from posts_player""")
	columns = [col[0] for col in cursor.description]
	players = [dict(zip(columns, row)) for row in cursor.fetchall()]

	context = {
		'title': 'Players in Database',
		'players': players
	}

	return render(request, 'posts/index.html', context)

def player(request, id):
	cursor = connection.cursor()
	cursor.execute("select * from posts_player where account_id = 'player" + id + "'")

	columns = [col[0] for col in cursor.description]
	player = [dict(zip(columns, row)) for row in cursor.fetchall()]
	context = {
		'player': player	
	}

	return render(request, 'posts/playerhome.html', context)

def playerauth(request, id):
	cursor = connection.cursor()
	cursor.execute("select * from posts_player where account_id = 'player" + id + "'")
	columns = [col[0] for col in cursor.description]
	player = [dict(zip(columns, row)) for row in cursor.fetchall()]
	context = {
		'player': player	
	}

	return render(request, 'posts/playerauthhome.html', context)

def form_player(request): 
	cursor = connection.cursor()
	cursor.execute("select * from posts_team")
	columns = [col[0] for col in cursor.description]
	teams = [dict(zip(columns, row)) for row in cursor.fetchall()]
	context = {
		"teams": teams
	}

	return render(request, 'posts/form_player.html', context)

def player_register(request):
	account_id = request.GET["account_id"]
	password = request.GET["password"]
	name = request.GET["name"]
	surname = request.GET["surname"]
	nationality = request.GET["nationality"]
	age = request.GET["age"]
	kit_no = request.GET["kit_no"]
	pref_foot = request.GET["pref_foot"]
	prev_transfer_fee = request.GET["prev_transfer_fee"]
	recdate = request.GET["recdate"]
	susdate = request.GET["susdate"]
	team = request.GET["team"]

	query = """INSERT INTO posts_player (account_id, password, name, surname, nationality, age, kit_no, pref_foot, prev_transfer_fee, recovery_date, suspend_date, belong_to_team_name) 
		VALUES ('""" + account_id + "', '" + password + "', '" + name + "', '" + surname + "', '" + str(nationality) + "', "
	query2 = str(age) + ", " + str(kit_no) + ", '" + str(pref_foot) + "', " + str(prev_transfer_fee) + ", "
	query3 = "STR_TO_DATE('" + str(recdate) + "', '%d/%m/%Y'), " + "STR_TO_DATE('" + str(susdate) + "', '%d/%m/%Y'), '" + str(team) + "');"

	sql = query + query2 + query3

	cursor = connection.cursor()
	cursor.execute(sql)

	transaction.commit()

	cursor.execute("select * from posts_player")
	columns = [col[0] for col in cursor.description]
	players = [dict(zip(columns, row)) for row in cursor.fetchall()]
	context = {
		'title': 'Players in Database',
		'players': players,
	}

	return render(request, 'posts/index.html', context)
	
def agent(request, id):
	cursor = connection.cursor()
	cursor.execute("select * from posts_agent where account_id = 'agent" + id + "'")
	columns = [col[0] for col in cursor.description]
	agent = [dict(zip(columns, row)) for row in cursor.fetchall()]
	context = {
		'agent': agent,
	}

	return render(request, 'posts/agenthome.html', context)

def agentauth(request, id):
	cursor = connection.cursor()
	cursor.execute("select * from posts_agent where account_id = 'agent" + id + "'")
	columns = [col[0] for col in cursor.description]
	agent = [dict(zip(columns, row)) for row in cursor.fetchall()]
	context = {
		'agent': agent,
	}

	return render(request, 'posts/agentauthhome.html', context)

def form_agent(request): 
	cursor = connection.cursor()
	cursor.execute("select * from posts_player")
	columns = [col[0] for col in cursor.description]
	players = [dict(zip(columns, row)) for row in cursor.fetchall()]
	context = {
		"players": players,
	}

	return render(request, 'posts/form_agent.html', context)

def agent_register(request):
	account_id = request.GET["account_id"]
	password = request.GET["password"]
	name = request.GET["name"]
	surname = request.GET["surname"]
	nationality = request.GET["nationality"]
	age = request.GET["age"]
	player = request.GET["player"]

	query = "INSERT INTO posts_agent (account_id, password, name, surname, nationality, player_id, age) VALUES ('"
	query2 = account_id + "', '" + password + "', '" + name + "', '" + surname + "', '" + str(nationality) + "', '" + str(player) + "', " + str(age) + ");"

	sql = query + query2

	cursor = connection.cursor()
	cursor.execute(sql)

	transaction.commit()

	cursor.execute("""select account_id, name, surname, nationality, age, kit_no, pref_foot, 
		prev_transfer_fee, recovery_date, suspend_date, belong_to_team_name from posts_player""")
	columns = [col[0] for col in cursor.description]
	players = [dict(zip(columns, row)) for row in cursor.fetchall()]
	context = {
		'title': 'Players in Database',
		'players': players,
	}

	return render(request, 'posts/index.html', context)

def president(request, id):
	cursor = connection.cursor()
	cursor.execute("select * from posts_president where account_id = 'president" + id + "'")
	columns = [col[0] for col in cursor.description]
	president = [dict(zip(columns, row)) for row in cursor.fetchall()]
	context = {
		'president': president,
	}

	return render(request, 'posts/presidenthome.html', context)

def presidentauth(request, id):
	cursor = connection.cursor()
	cursor.execute("select * from posts_president where account_id = 'president" + id + "'")
	columns = [col[0] for col in cursor.description]
	president = [dict(zip(columns, row)) for row in cursor.fetchall()]
	context = {
		'president': president,
	}

	return render(request, 'posts/presidentauthhome.html', context)

def form_president(request): 
	cursor = connection.cursor()
	cursor.execute("select * from posts_team")
	columns = [col[0] for col in cursor.description]
	teams = [dict(zip(columns, row)) for row in cursor.fetchall()]
	context = {
		"teams": teams,
	}

	return render(request, 'posts/form_president.html', context)

def president_register(request):
	account_id = request.GET["account_id"]
	password = request.GET["password"]
	name = request.GET["name"]
	surname = request.GET["surname"]
	nationality = request.GET["nationality"]
	age = request.GET["age"]
	startdate = request.GET["startdate"]
	team = request.GET["team"]

	query = "INSERT INTO posts_president (account_id, password, name, surname, nationality, age, start_date, team_name) VALUES ('"
	query2 = account_id + "', '" + password + "', '" + name + "', '" + surname + "', '" + str(nationality) + "', " + str(age) + ", "
	query3 = "STR_TO_DATE('" + str(startdate) + "', '%d/%m/%Y'), '" + str(team) + "')"
	sql = query + query2 + query3

	cursor = connection.cursor()
	cursor.execute(sql)

	transaction.commit()

	cursor.execute("""select account_id, name, surname, nationality, age, kit_no, pref_foot, 
		prev_transfer_fee, recovery_date, suspend_date, belong_to_team_name from posts_player""")
	columns = [col[0] for col in cursor.description]
	players = [dict(zip(columns, row)) for row in cursor.fetchall()]
	context = {
		'title': 'Players in Database',
		'players': players,
	}

	return render(request, 'posts/index.html', context)


def coach(request, id):
	cursor = connection.cursor()
	cursor.execute("select * from posts_coach where account_id = 'coach" + id + "'")
	columns = [col[0] for col in cursor.description]
	coach = [dict(zip(columns, row)) for row in cursor.fetchall()]
	context = {
		'coach': coach,
	}

	return render(request, 'posts/coachhome.html', context)

def coachauth(request, id):
	cursor = connection.cursor()
	cursor.execute("select * from posts_coach where account_id = 'coach" + id + "'")
	columns = [col[0] for col in cursor.description]
	coach = [dict(zip(columns, row)) for row in cursor.fetchall()]
	context = {
		'coach': coach,
	}

	return render(request, 'posts/coachauthhome.html', context)

def form_coach(request): 
	cursor = connection.cursor()
	cursor.execute("select * from posts_team")
	columns = [col[0] for col in cursor.description]
	teams = [dict(zip(columns, row)) for row in cursor.fetchall()]
	context = {
		"teams": teams,
	}

	return render(request, 'posts/form_coach.html', context)

def coach_register(request):
	account_id = request.GET["account_id"]
	password = request.GET["password"]
	name = request.GET["name"]
	surname = request.GET["surname"]
	nationality = request.GET["nationality"]
	age = request.GET["age"]
	startdate = request.GET["startdate"]
	team = request.GET["team"]

	query = "INSERT INTO posts_coach (account_id, password, name, surname, nationality, age, start_date, team_name) VALUES ('"
	query2 = account_id + "', '" + password + "', '" + name + "', '" + surname + "', '" + str(nationality) + "', " + str(age) + ", "
	query3 = "STR_TO_DATE('" + str(startdate) + "', '%d/%m/%Y'), '" + str(team) + "')"
	sql = query + query2 + query3

	cursor = connection.cursor()
	cursor.execute(sql)

	transaction.commit()

	cursor.execute("""select account_id, name, surname, nationality, age, kit_no, pref_foot, 
		prev_transfer_fee, recovery_date, suspend_date, belong_to_team_name from posts_player""")
	columns = [col[0] for col in cursor.description]
	players = [dict(zip(columns, row)) for row in cursor.fetchall()]
	context = {
		'title': 'Players in Database',
		'players': players,
	}

	return render(request, 'posts/index.html', context)

def league(request):
    cursor = connection.cursor()
    cursor.execute("SELECT distinct league FROM posts_team")
    columns = [col[0] for col in cursor.description]
    league = [dict(zip(columns, row)) for row in cursor.fetchall()]
    context = {
        'league': league,
    }

    return render(request, 'posts/league.html', context)


def leagues_info(request, string):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT team_name, points, win_count, draw_count, loss_count" +
        "FROM posts_team NATURAL JOIN SELECT teams.team_name, " +
            "IFNULL(team_wins.win_count, 0) win_count, " +
            "IFNULL(team_draws.draw_count, 0) draw_count, " +
            "IFNULL(team_losses.loss_count, 0) loss_count, " +
            "IFNULL(team_wins.win_count, 0) * 3 + IFNULL(team_draws.draw_count, 0) points" +
            "FROM (  SELECT team_name FROM team_wins UNION" +
            "SELECT team_name FROM team_draws UNION" +
            "SELECT team_name FROM team_losses ) teams" +
            "LEFT JOIN team_wins ON teams.team_name = team_wins.team_name" +
            "LEFT JOIN team_draws ON teams.team_name = team_draws.team_name" +
            "LEFT JOIN team_losses ON teams.team_name = team_losses.team_name" +
        "WHERE posts_team.league = '" + string + "'" +
        "ORDER BY points DESC")

    columns = [col[0] for col in cursor.description]
    league_standings = [dict(zip(columns, row)) for row in cursor.fetchall()]
    context = {
        'league_standings': league_standings,
    }

    return render(request, 'posts/standings.html', context)

