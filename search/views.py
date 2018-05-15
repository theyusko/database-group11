from django.shortcuts import render
from django.db import connection,transaction
from django.http import Http404
from django.http import HttpResponse

def index(request):
    context = {}
    return render(request, 'search/search.html', context)

def teams(request):
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT team_name FROM team")
    columns = [col[0] for col in cursor.description]
    team_names = [dict(zip(columns, row)) for row in cursor.fetchall()]
    context = {
        'team_names': team_names,
    }

    return render(request, 'search/register.html', context)

def process_query(request):
    cursor = connection.cursor()
    name = request.GET["nameInput"]
    display_type = request.GET["types"]

    if display_type in ["player", "coach", "president", "agent", "team", "match"]:
        if display_type == "player":
            nationality = request.GET["player-nationalityInput"]
            minAge = request.GET["player-minAgeInput"]
            maxAge = request.GET["player-maxAgeInput"]
            playerPlaysIn = request.GET["player-playsInInput"]
            playerBelongsTo = request.GET["player-belongsToInput"]
            positions1 = request.GET["player-positionsInput1"]
            positions2 = request.GET["player-positionsInput2"]
            total_goals = request.GET["player-totalGoalsInput"]
            total_assists = request.GET["player-totalAssistsInput"]
            tables_used = [0, 0, 0, 0]  # Indicates if goals_of_player, assists_of_player, positions, plays_in tables are used

            if total_assists == "" and total_goals == "":
                player_comprehensive = "(select player.account_id, player.name, player.surname, " \
                                       "player.nationality, player.age, player.kit_no, player.belong_to_team_name, " \
                                       "player.pref_foot, player.birthdate, positions.position, plays_in.team_name from " \
                                       "( select account_id from player union " \
                                       "select account_id from positions union " \
                                       "select account_id from plays_in ) ids " \
                                       "left join player on ids.account_id = player.account_id " \
                                       "left join positions on ids.account_id = positions.account_id " \
                                       "left join plays_in on ids.account_id = plays_in.account_id) as player_compr"
            else:
                cursor.execute("DROP VIEW IF EXISTS goals_of_player")
                cursor.execute("CREATE VIEW goals_of_player "
                               "AS SELECT player.account_id as account_id , SUM(value) as goals "
                               "FROM statistics, player WHERE statistics.account_id = player.account_id AND statistics.type = 'goal' GROUP BY player.account_id")
                cursor.execute("DROP VIEW IF EXISTS assists_of_player")
                cursor.execute("CREATE VIEW assists_of_player "
                               "AS SELECT player.account_id as account_id, SUM(value) as assists "
                               "FROM statistics, player WHERE statistics.account_id = player.account_id AND statistics.type = 'assist' GROUP BY player.account_id")
                player_comprehensive = "(select player.account_id, player.name, player.surname, " \
                                       "player.nationality, player.age, player.kit_no, player.belong_to_team_name, " \
                                       "player.pref_foot, player.birthdate, positions.position, plays_in.team_name, " \
                                       "goals_of_player.goals, assists_of_player.assists from " \
                                       "( select account_id from player union " \
                                       "select account_id from positions union " \
                                       "select account_id from plays_in union " \
                                       "select account_id from goals_of_player union " \
                                       "select account_id from assists_of_player ) as ids " \
                                       "left join player on ids.account_id = player.account_id" \
                                       " left join positions on ids.account_id = positions.account_id " \
                                       "left join plays_in on ids.account_id = plays_in.account_id " \
                                       "left join goals_of_player on ids.account_id = goals_of_player.account_id " \
                                       "left join assists_of_player on ids.account_id = assists_of_player.account_id) as player_compr"
            sqlQuery = "select player_compr.name, player_compr.surname, player_compr.account_id " \
                        "from" + player_comprehensive +" " \
                        "WHERE (player_compr.name LIKE '" + name + "%%' OR player_compr.surname LIKE '" + name + "%%')"

            if nationality != "":
                sqlQuery += " AND player_compr.nationality = '" + nationality + "'"
            if minAge != "" and maxAge != "":
                sqlQuery += " AND (player_compr.age BETWEEN " + minAge + " AND " + maxAge + ")"
            if playerBelongsTo != "":
                sqlQuery += " AND player_compr.belong_to_team_name LIKE '" + playerBelongsTo + "%%'"
            if playerPlaysIn != "":
                sqlQuery += " AND player_compr.team_name LIKE '" + playerPlaysIn + "%%" + "'"
                tables_used[3] = 1
            if positions1 != "":
                sqlQuery += " AND player_compr.position = '" + positions1 + "'"
                tables_used[2] = 1
            if positions2 != "":
                sqlQuery += " AND player_compr.position = '" + positions2 + "'"
                tables_used[2] = 1
            if total_goals != "":
                tables_used[0] = 1
                sqlQuery += " AND player_compr.goals = '" + total_goals + "'"
            if total_assists != "":
                tables_used[1] = 1
                sqlQuery += " AND player_compr.assists = '" + total_assists + "'"

            #if tables_used[0]:
            #    sqlQuery += " AND player.account_id = goals_of_player.account_id"
            #if tables_used[1]:
            #    sqlQuery += " AND player.account_id = assists_of_player.account_id"
            #if tables_used[2]:
            #    sqlQuery += " AND player.account_id = positions.account_id"
            #if tables_used[3]:
            #   sqlQuery += " AND player.account_id = plays_in.account_id"

            sqlQuery += ";"
            cursor.execute(sqlQuery)
            columns = [col[0] for col in cursor.description]
            players = [dict(zip(columns, row)) for row in cursor.fetchall()]
            context = {
                'title': 'Search Results',
                'players': players,
            }

            return render(request, 'search/search_results_player.html', context)

        elif display_type == "agent":
            a_nationality = request.GET["agent-nationalityInput"]
            players_name = request.GET["agent-presentingPlayerNameInput"]

            sqlQuery = "select agent.name, agent.surname, agent.account_id " \
                       "from player, agent where player.account_id = agent.player_account_id" \
                       "AND (agent.name LIKE '" + name + "%%" + "' OR agent.surname LIKE '" + name + "%%" + "')"

            if a_nationality != "":
                sqlQuery += " AND agent.nationality = '" + a_nationality + "'"
            if players_name != "":
                sqlQuery += " AND (player.name LIKE '" + players_name + "%%" + "' OR player.surname LIKE '" + players_name + "%%" + "')"

            sqlQuery += ";"
            cursor.execute(sqlQuery)
            columns = [col[0] for col in cursor.description]
            agents = [dict(zip(columns, row)) for row in cursor.fetchall()]
            context = {
                'title': 'Search Results',
                'agents': agents,
            }
            return render(request, 'search/search_results_agent.html', context)

        elif display_type == "coach":
            c_nationality = request.GET["coach-nationalityInput"]
            c_team = request.GET["coach-teamNameInput"]

            sqlQuery = "select coach.name, coach.surname, coach.account_id " \
                       "from coach, team where coach.team_name = team.team_name" \
                       " AND (coach.name LIKE '" + name + "%%" + "' OR coach.surname LIKE '" + name + "%%')"

            if c_nationality != "":
                sqlQuery += " AND coach.nationality = '" + c_nationality + "'"
            if c_team != "":
                sqlQuery += " AND coach.team_name = '" + c_team + "'"

            sqlQuery += ";"
            cursor.execute(sqlQuery)
            columns = [col[0] for col in cursor.description]
            coach = [dict(zip(columns, row)) for row in cursor.fetchall()]
            context = {
                'title': 'Search Results',
                'coach': coach,
            }
            return render(request, 'search/search_result_coach.html', context)

        elif display_type == "president":
            p_nationality = request.GET["president-nationalityInput"]
            p_team = request.GET["president-teamNameInput"]

            sqlQuery = "select president.name, president.surname, president.account_id, president.team_name " \
                       "from president, team where team.team_name = president.team_name"

            sqlQuery += " AND (president.name LIKE '" + name + "%%' OR president.surname LIKE '" + name + "%%" + "')"

            if p_nationality != "":
                sqlQuery += " AND president.nationality = '" + p_nationality + "'"
            if p_team != "":
                sqlQuery += " AND president.team_name = '" + p_team + "'"

            cursor.execute(sqlQuery)
            columns = [col[0] for col in cursor.description]
            president = [dict(zip(columns, row)) for row in cursor.fetchall()]
            context = {
                'title': 'Search Results',
                'president': president,
            }
            return render(request, 'search/search_results_president.html', context)

        elif display_type == "team":
            city = request.GET["team-cityInput"]
            league = request.GET["team-leagueInput"]
            stadium = request.GET["team-stadiumNameInput"]
            budget = request.GET["team-budgetInput"]

            sqlQuery = "SELECT team.team_name FROM team WHERE team.team_name LIKE '" + name + "%%'"

            if league != "":
                sqlQuery += " AND team.league = LIKE '" + league + "%%'"
            if stadium != "":
                sqlQuery += " AND team.stadium_name = LIKE '%%" + stadium + "%%'"
            if budget != "":
                sqlQuery += " AND team.budget > " + budget
            if city != "":
                sqlQuery += " AND president.city = LIKE '%%" + stadium + "%%'"

            cursor.execute(sqlQuery)
            columns = [col[0] for col in cursor.description]
            team = [dict(zip(columns, row)) for row in cursor.fetchall()]
            context = {
                'title': 'Search Results',
                'team': team,
            }

            return render(request, 'search/search_results_team.html', context)

        elif display_type == "match":
            league = request.GET["matchLeagueInput"]
            other_team = request.GET["match-otherTeamNameInput"]

            sqlQuery = "SELECT DISTINCT match_id, home_team, guest_team, home_score, guest_score FROM matches, team "

            if other_team == "":
                sqlQuery += "WHERE home_team LIKE '" + name + "%%' OR guest_team LIKE '" + name + "%%'"
            if other_team != "":
                sqlQuery += "WHERE ( home_team LIKE '" + name + "%%' AND guest_team LIKE '" + other_team + "%%' ) "\
                            "OR ( home_team LIKE '" + other_team + "%%' AND guest_team LIKE '" + name + "%%' )"

            if league != "":
                sqlQuery += " AND ( team.team_name = matches.home_team AND team.league LIKE '" + league + "%%')"

            sqlQuery += ";"
            cursor.execute(sqlQuery)
            columns = [col[0] for col in cursor.description]
            match = [dict(zip(columns, row)) for row in cursor.fetchall()]
            context = {
                'title': 'Search Results',
                'match': match,
            }
            return render(request, 'search/search_results_match.html', context)




    else:
        return Http404("Type Error")

