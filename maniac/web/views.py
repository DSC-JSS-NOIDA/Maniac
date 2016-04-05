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

def about_us(request):
    return render(request, 'web/aboutus.html')
