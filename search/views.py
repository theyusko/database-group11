from django.shortcuts import render
from django.db import connection,transaction
from django.http import Http404
from django.http import HttpResponse

def index(request):
    context = {}
    return render(request, 'search/search.html', context)

def process_query(request):
    name = request.GET["name"]
    surname = request.GET["surname"]
    display_type = request.GET["types"]
    nationality = request.GET["nationality"]
    minAge = request.GET["minAgeInput"]
    maxAge = request.GET["maxAgeInput"]
    playerBelongsTo = request.GET["playerBelongsToInput"]
    playerPlaysIn = request.GET["playerPlaysInInput"]

    playerBirthdate = request.GET["playerBirthdateInput"] #Return the input as YYYY-MM-DD

    playerTotalGoals = request.GET["playerTotalGoalsInput"]
    playerTotalAssist = request.GET["playerTotalAssistsInput"]

    positions1 = request.GET["positions1[]"]
    positions2 = request.GET["positions2[]"]

    cursor = connection.cursor()

    if display_type in ["player", "coach", "president", "agent", "team", "match"]:
        if display_type == "player":
            sqlQuery = "select * from posts_player as player, posts_statistics as statistics, posts_position as positions, posts_playsin as playsin " \
                       "where player.account_id = statistics.player_id AND statistics.player_id = positions.account_id AND positions.account_id = playsin.account_id"

            sqlQuery += " AND player.name LIKE '" + name + "%%" + "'"
            sqlQuery += " AND player.surname LIKE '" + surname + "%%" + "'"
            if nationality != "":
                sqlQuery += " AND player.nationality = '" + nationality + "'"
            if minAge != "":
                sqlQuery += " AND player.age BETWEEN " + minAge + " AND " + maxAge
            if playerBelongsTo != "":
                sqlQuery += " AND player.belong_to_team_name LIKE '" + playerBelongsTo + "%%'"
            if playerPlaysIn != "":
                sqlQuery += " AND playsin.team_name LIKE '" + playerPlaysIn + "%%" + "'"
            if positions1 != "":
                sqlQuery += " AND positions.position = '" + positions1 + "'"
            if positions2 != "":
                sqlQuery += " AND positions.position = '" + positions2 + "'"

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
            agentNationality = request.GET["agentNationalityInput"]
            agentPresentingPlayerName = request.GET["agentPresentingPlayerNameInput"]

            sqlQuery = "select agent.name, agent.surname, agent.account_id from posts_player as player, posts_agent as agent where player.account_id = agent.player_id"

            sqlQuery += " AND agent.name LIKE '" + name + "%%" + "'"
            sqlQuery += " AND agent.surname LIKE '" + surname + "%%" + "'"

            if agentNationality != "":
                sqlQuery += " AND agent.nationality = '" + nationality + "'"
            if agentPresentingPlayerName != "":
                sqlQuery += " AND agent.player_id = '" + agentPresentingPlayerName + "'"

            cursor.execute(sqlQuery)
            columns = [col[0] for col in cursor.description]
            agents = [dict(zip(columns, row)) for row in cursor.fetchall()]
            context = {
                'title': 'Search Results',
                'agents': agents,
            }
            return render(request, 'search/search_results_agent.html', context)


        elif display_type == "coach":
            coachNationality = request.GET["coachNationalityInput"]
            coachTeam = request.GET["coachTeamInput"]

            #Not implemented
            coachContractStartDate = request.GET["coachTeamInput"]

            sqlQuery = "select coach.name, coach.surname, coach.account_id, coach.team_name from posts_coach as coach, posts_team as team where team.team_name = coach.team_name"

            sqlQuery += " AND coach.name LIKE '" + name + "%%" + "'"
            sqlQuery += " AND coach.surname LIKE '" + surname + "%%" + "'"

            if coachNationality != "":
                sqlQuery += " AND coach.nationality = '" + coachNationality + "'"
            if coachTeam != "":
                sqlQuery += " AND coach.team_name = '" + coachTeam + "'"

            cursor.execute(sqlQuery)
            columns = [col[0] for col in cursor.description]
            coach = [dict(zip(columns, row)) for row in cursor.fetchall()]
            context = {
                'title': 'Search Results',
                'coach': coach,
            }
            return render(request, 'search/search_result_coach.html', context)


    else:
        return Http404("Type Error")