from django.contrib import admin
from .models import *
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('description', 'answer', 'created', 'modified')

admin.site.register(Question, QuestionAdmin)


class QuestionSolvedAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'answer', 'created', 'modified')

admin.site.register(QuestionSolved, QuestionSolvedAdmin)


class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'college', 'phone_number', 'score', 'created', 'modified')

admin.site.register(UserDetail, UserDetailAdmin)
