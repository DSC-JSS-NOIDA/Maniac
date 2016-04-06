from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserDetail(models.Model):
    user = models.OneToOneField(User)
    college = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    score = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)


class Question(models.Model):
    descripton = models.TextField()
    answer = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)


class QuestionSolved(models.Model):
    question = models.ForeignKey(Question, related_name='question')
    user = models.ForeignKey(User, related_name='user')
    answer = models.CharField(max_length=10000, blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)
