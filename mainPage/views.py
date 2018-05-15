from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection,transaction

from django.shortcuts import render
from django.db import connection,transaction
from django.http import Http404
from django.http import HttpResponse

def index(request):
    return render(request, 'mainPage/mainPage.html', {})

def authenticatedMainPage(request):
    return

