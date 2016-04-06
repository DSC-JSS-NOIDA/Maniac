from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, render
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.db.models import Q
from django.core.urlresolvers import reverse_lazy

import utils.constants as constants
from datetime import datetime, timedelta

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
        if request.method == "POST":
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            name = request.POST['name']
            college = request.POST['college']
            phno = request.POST['phno']
            try:
                user = User.objects.create_user(username=username,email=email,password=password,first_name=name,last_name='')
                user.save()
                UserDetail.objects.create(user = user, college = college, phone_number = phno).save()
                return HttpResponseRedirect(reverse_lazy('login'))
            except:
                return render(request, "web/register.html",{"error":"Hmm....I think you are already registered."})
        else:
            return render(request, "web/register.html")
    else:
        return HttpResponseRedirect(reverse_lazy('index'))    


def login(request):
    if not request.user.is_authenticated():
        if request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request,user)
                return HttpResponseRedirect(reverse_lazy('questions'))
            else:
                return render(request, "web/login.html",{"error":"Can you try with the correct credentials ??"})
        return render(request, 'web/login.html')
    else:
        return HttpResponseRedirect(reverse_lazy('questions'))


def question(request):
    if request.user.is_authenticated():
        user = User.objects.get(id=request.user.id)
        if request.method == "GET":
            last_solved_question = QuestionSolved.objects.filter(user__id=user.id).order_by('-created')
            start_date = timezone.now().date()
            end_date = start_date + timedelta( days=1 )
            # calculate the number of questions solved today
            questions_solved_today = QuestionSolved.objects.filter(user__id=user.id, created__range=(start_date, end_date))
            total_questions_solved_by_user = QuestionSolved.objects.filter(user__id=user.id).filter(~Q(answer=None))
            total_questions = QuestionSolved.objects.all().count()
            # check if user has already solved all the questions
            if total_questions == total_questions_solved_by_user:
                return render(request, 'web/finish.html')

            date_when_user_joined = user.date_joined
            delta_days = (timezone.now().date()-date_when_user_joined).days
            # check if the user has solved all the questions to be displayed today only
            if questions_solved_today.count() >= (delta_days+1)*constants.QUESTIONS_TO_BE_SOLVED_IN_A_DAY:
                return render(request, 'web/question.html', {'warning': 'You are done for the day. Come next day to continue the contest.'})
            else:
                next_question = Question.objects.get(id=last_solved_question+1)
                if QuestionSolved.objects.filter(user=user, question__id=next_question.id).count()==0:
                    QuestionSolved.objects.create(user=user, question__id=next_question.id)
                    user.last_login=timezone.now()
                    user.save()

                return render(request, 'web/question.html', {'question': next_question, 'time_to_show': user.last_login})
        elif request.method == "POST":
            answer = request.POST.get('answer', None)
            question_id = request.POST.get('question_id', None)
            corresponding_question = QuestionSolved.objects.get(user=user, question__id=question_id)
            # to handle the case of the developers trying to make POST request to the urls
            if corresponding_question.answer == None:
                QuestionSolved.objects.get(user=user, question__id=question_id).update(answer=answer)
                return HttpResponseRedirect(reverse_lazy('questions'))
            else:
                return render(request, 'web/question.html', {'warning': 'You are trying to be smart enough. But, I am more smart than you :P'})

def about(request):
    return render(request, 'web/about.html')


def leaderboard(request):
    users = UserDetail.objects.order_by('-CurrentQuestionNo')[:7:1]
    return render_to_response("leaderboard.html",{'users':users},context_instance = RequestContext(request))
