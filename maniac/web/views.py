from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, render
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.db.models import Q
from django.core.urlresolvers import reverse_lazy
from django.contrib import auth
from django.contrib.auth import logout

from web.models import UserDetail, Question, QuestionSolved

from datetime import datetime, timedelta
from django.utils import timezone

import time
import math
import datetime
import re
import utils.constants as constants


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
            print request.POST
            try:
                user = User.objects.create_user(username=username,email=email,password=password,first_name=name,last_name='')
                UserDetail.objects.create(user=user, college=college, phone_number=phno)
                return HttpResponseRedirect(reverse_lazy('login'))
            except:
                return render(request, "web/register.html",{"error": "Hmm....Someone has already used that username. Try some other username."})
        else:
            return render(request, "web/register.html")
    else:
        return HttpResponseRedirect(reverse_lazy('index'))    


def login(request):
    if not request.user.is_authenticated():
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            print request.POST
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request,user)
                return HttpResponseRedirect(reverse_lazy('questions'))
            else:
                return render(request, "web/login.html",{"error":"Username password mismatch. Can you try with the correct credentials ??"})
        return render(request, 'web/login.html')
    else:
        return HttpResponseRedirect(reverse_lazy('questions'))


def question(request):
    if request.user.is_authenticated():
        user = User.objects.get(id=request.user.id)
        if request.method == "GET":
            try:
                last_solved_question = QuestionSolved.objects.filter(user__id=user.id).filter(~Q(answer=None)).order_by('-created')[0]
                last_solved_question_id = last_solved_question.question.id
            except:
                last_solved_question_id = 0
            # print "#################    ", last_solved_question_id
            start_date = timezone.now().date()
            end_date = start_date + timedelta( days=1 )
            # calculate the number of questions solved
            # questions_solved_today = QuestionSolved.objects.filter(user__id=user.id, created__range=(start_date, end_date))
            total_questions_solved_by_user = QuestionSolved.objects.filter(user__id=user.id).filter(~Q(answer=None)).count()
            total_questions = Question.objects.all().count()
            # check if user has already solved all the questions
            if total_questions == total_questions_solved_by_user:
                return render(request, 'web/finish.html')

            date_when_user_joined = timezone.localtime(user.date_joined).date()
            event_start_date = datetime.datetime.strptime(constants.START_DATE, '%d/%m/%Y').date()
            delta_days = (timezone.localtime(timezone.now()).date() - event_start_date).days
            # check if the user has solved all the questions to be displayed today only
            # print "THRESHOLD IS ", (delta_days+1)*constants.QUESTIONS_TO_BE_SOLVED_IN_A_DAY
            if total_questions_solved_by_user >= (delta_days+1)*constants.QUESTIONS_TO_BE_SOLVED_IN_A_DAY:
                return render(request, 'web/question.html', {'warning': 'You are done for the day. Come next day to continue the contest.'})
            else:
                next_question = Question.objects.get(id=last_solved_question_id+1)
                if QuestionSolved.objects.filter(user=user, question__id=next_question.id).count()==0:
                    QuestionSolved.objects.create(user=user, question=next_question)
                    user.last_login=timezone.now()
                    user.save()

                return render(request, 'web/question.html', {'question': next_question, 'time_to_show': user.last_login})
        elif request.method == "POST":
            answer = request.POST.get('answer', None)
            question_id = request.POST.get('question_id', None)
            corresponding_question = QuestionSolved.objects.get(user=user, question__id=question_id)
            time_diff = (timezone.now()-timezone.localtime(corresponding_question.created)).total_seconds()/60
            time_based_score = constants.TIME_BASED_SCORE_MAX_VALUE/math.ceil(time_diff)
            # to handle the case of the developers trying to make POST request to the urls
            if corresponding_question.answer == None:
                QuestionSolved.objects.filter(user=user, question__id=question_id).update(answer=answer, time_based_score=time_based_score)
                return render(request, 'web/continue.html')
            else:
                return render(request, 'web/over_smart.html')


def leaderboard(request):
    users = UserDetail.objects.order_by('-CurrentQuestionNo')[:7:1]
    return render_to_response("leaderboard.html",{'users':users},context_instance = RequestContext(request))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))
