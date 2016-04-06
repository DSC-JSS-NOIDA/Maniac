from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, render
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from datetime import timedelta
import time
import datetime
import re

from django.conf import settings

# Create your views here.


def index(request):
    return render(request, 'web/index.html', {"static_url": settings.STATIC_URL})


def rules(request):
    return render(request, 'web/rules.html')


def register(request):
    if not request.user.is_active:
        if request.POST:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            name = request.POST['firstname']
            college = request.POST['college']
            phno = request.POST['phno']
            try:
                user = User.objects.create_user(username=username,email=email,password=password,first_name=name,last_name='')
                user.save()
                UserDetail.objects.create(user = suser, college = college, phone_number = phno).save()
                return HttpResponseRedirect("/login")
            except:
                return render_to_response("web/register.html",{"error":"Hmm....I think you are already registered."},context_instance = RequestContext(request))
        else:
            return render_to_response("web/register.html",context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/")    


def login(request):
    if not request.user.is_authenticated():
        if request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request,user)
                return HttpResponseRedirect("/google-it")
            else:
                return render_to_response("login.html",{"error":"Can you try with the correct credentials ??"},context_instance = RequestContext(request))
        return render_to_response('login.html',context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/google-it")


def question(request, question=1):
    if request.user.is_authenticated():
        if request.method == "GET":
            user = request.user
            last_solved_question = QuestionSolved.objects.filter(user__id=request.user.id).order_by('-created')
            start_date = timezone.now().date()
            end_date = start_date + timedelta( days=1 )
            questions_solved_today = QuestionSolved.objects.filter(user__id=request.user.id, created__range=(start_date, end_date))
            if questions_solved_today.count() >= 10:
                return render(request, 'question.html', {'warning': 'You are done for the day. Come after 00:00 hours'})
            else:
                next_question = Question.objects.get(id=last_solved_question+1)
                if QuestionSolved.objects.filter(user=request.user, question__id=next_question.id).count()==0:
                    QuestionSolved.objects.create(user=request.user, question__id=next_question.id)
                    user = User.objects.get(id=request.user.id)
                    user.last_login=timezone.now()
                    user.save()
                    return render(request, 'question.html', {'question': next_question, 'time_to_show': user.last_login})
                else:
                    pass
                return render(request, 'question.html', {'question': next_question})
    return render(request, 'web/question.html',{})

def about(request):
    return render(request, 'web/about.html')


def leader_board(request):
    users = UserDetail.objects.order_by('-CurrentQuestionNo')[:7:1]
    return render_to_response("leaderboard.html",{'users':users},context_instance = RequestContext(request))
