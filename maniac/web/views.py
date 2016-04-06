from django.shortcuts import render
import time
import datetime
import re

from django.conf import settings

# Create your views here.

def index(request):
    return render(request, 'web/index.html', {"static_url": settings.STATIC_URL})

def leader_board(request):
    return render(request, 'web/leaderboard.html')

def rules(request):
    return render(request, 'web/rules.html')

def register(request):
    return render(request, 'web/register.html')

def login(request):
    return render(request, 'web/login.html')

def about(request):
    return render(request, 'web/about.html')
