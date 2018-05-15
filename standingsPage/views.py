from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection,transaction


def league(request):
    cursor = connection.cursor()
    cursor.execute("SELECT distinct league FROM team")
    columns = [col[0] for col in cursor.description]
    league = [dict(zip(columns, row)) for row in cursor.fetchall()]
    context = {
        'league': league,
    }

    return render(request, 'standingsPage/selectLeague.html', context)


def league_standings(request, league):
    cursor = connection.cursor()
    cursor.execute("DROP VIEW IF EXISTS team_wins")
    cursor.execute("DROP VIEW IF EXISTS team_draws")
    cursor.execute("DROP VIEW IF EXISTS team_losses")

    cursor.execute("DROP VIEW IF EXISTS team_names")
    cursor.execute("CREATE VIEW team_names(team_name) AS SELECT DISTINCT team_name FROM team")
    cursor.execute("CREATE VIEW team_wins(team_name, win_count) AS SELECT team_name, count(match_id) AS win_count FROM matches, team_names WHERE ( home_team = team_name AND home_score > guest_score ) OR ( guest_team = team_name AND home_score < guest_score ) GROUP BY team_name")
    cursor.execute("CREATE VIEW team_draws(team_name, draw_count) AS SELECT team_name, count(match_id) AS draw_count FROM matches, team_names WHERE ( home_team = team_name OR guest_team = team_name ) AND home_score = guest_score GROUP BY team_name")
    cursor.execute("CREATE VIEW team_losses(team_name, loss_count) AS SELECT team_name, count(match_id) AS loss_count FROM matches, team_names WHERE ( home_team = team_name AND home_score < guest_score ) OR ( guest_team = team_name AND home_score > guest_score ) GROUP BY team_name")

    cursor.execute("SELECT team_name, points, win_count, draw_count, loss_count FROM team NATURAL JOIN (SELECT teams.team_name as team_name, IFNULL(team_wins.win_count, 0) win_count, IFNULL(team_draws.draw_count, 0) draw_count, IFNULL(team_losses.loss_count, 0) loss_count, IFNULL(team_wins.win_count, 0)*3 + IFNULL(team_draws.draw_count, 0) points FROM ( SELECT team_name FROM team_wins UNION SELECT team_name FROM team_draws UNION SELECT team_name FROM team_losses ) AS teams left join team_wins on teams.team_name = team_wins.team_name left join team_draws on teams.team_name = team_draws.team_name left join team_losses on teams.team_name = team_losses.team_name) as all_standings WHERE team.league = %s ORDER BY points DESC;", [league])

    columns = [col[0] for col in cursor.description]
    standings = [dict(zip(columns, row)) for row in cursor.fetchall()]
    context = {
        'league_standings': standings,
    }

    return render(request, 'standingsPage/standingsPage.html', context)


def match_history(request, league):
    cursor = connection.cursor()
    cursor.execute("SELECT home_team, home_score, gues_team, guest_score FROM matches, (SELECT team_name, league FROM team) as names WHERE home_team = team_name AND names.league = %s", [league])

    columns = [col[0] for col in cursor.description]
    hist = [dict(zip(columns, row)) for row in cursor.fetchall()]
    context = {
        'match_history': hist,
    }

    return render(request, 'standingsPage/standingsPage.html', context)