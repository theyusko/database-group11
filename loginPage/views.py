from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection,transaction

def index(request):
    cursor = connection.cursor()
    cursor.execute("""select account_id from posts_player""")
    columns = [col[0] for col in cursor.description]
    players = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.execute("""select account_id from posts_president""")
    columns = [col[0] for col in cursor.description]
    presidents = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.execute("""select account_id from posts_agent""")
    columns = [col[0] for col in cursor.description]
    agents = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.execute("""select account_id from posts_coach""")
    columns = [col[0] for col in cursor.description]
    coaches = [dict(zip(columns, row)) for row in cursor.fetchall()]

    context = {
        'warningTitle': '',
        'players': players,
        'agents': agents,
        'coaches': coaches,
        'presidents': presidents
    }

    return render(request, 'loginPage/loginPage.html', context)

def registerPage(request):
    return render(request, 'loginPage/loginPage.html', {})

def requestLogin(request):
    username = request.GET["username"]
    password = request.GET["password"]

    cursor = connection.cursor()
    cursor.execute("""select account_id, password from posts_player;""")
    columns = [col[0] for col in cursor.description]
    players = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.execute("""select account_id, password from posts_president;""")
    columns = [col[0] for col in cursor.description]
    presidents = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.execute("""select account_id, password from posts_agent;""")
    columns = [col[0] for col in cursor.description]
    agents = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.execute("""select account_id, password from posts_coach;""")
    columns = [col[0] for col in cursor.description]
    coaches = [dict(zip(columns, row)) for row in cursor.fetchall()]

    context = {
        'title': 'Players in Database',
        'players': players,
        'agents': agents,
        'coaches': coaches,
        'presidents': presidents
    }

    for x in players:
        if (username == (x.__getitem__('account_id'))) and (password == (x.__getitem__('password'))):
            return render(request, 'mainPage/playerMainPage.html', {'authenticatedUser': x})

    for x in agents:
        if (username == (x.__getitem__('account_id'))) and (password == (x.__getitem__('password'))):
            return render(request, 'mainPage/agentMainPage.html', {'authenticatedUser': x})

    for x in coaches:
        if (username == (x.__getitem__('account_id'))) and (password == (x.__getitem__('password'))):
            return render(request, 'mainPage/coachMainPage.html', {'authenticatedUser': x})

    for x in presidents:
        if (username == (x.__getitem__('account_id'))) and (password == (x.__getitem__('password'))):
            return render(request, 'mainPage/presidentMainPage.html', {'authenticatedUser': x})

        return render(request, 'loginPage/loginPage.html', {'warningTitle': 'ID and Password did not match. Please try again.'})


