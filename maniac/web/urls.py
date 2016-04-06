from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^leader-board/', views.leader_board, name="leader_board"),
    url(r'^rules/', views.rules, name="rules"),
    url(r'^register/', views.register, name="register"),
    url(r'^login/', views.login, name="login"),
    url(r'^question/', views.question, name="question"),

]
