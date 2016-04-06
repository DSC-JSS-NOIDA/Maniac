from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^leaderboard/', views.leaderboard, name="leaderboard"),
    url(r'^rules/', views.rules, name="rules"),
    url(r'^register/', views.register, name="register"),
    url(r'^login/', views.login, name="login"),
    url(r'^question/', views.question, name="questions"),

]
