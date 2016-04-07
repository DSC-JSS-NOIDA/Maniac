from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^leaderboard/', views.leaderboard, name="leaderboard"),
    url(r'^rules/', views.rules, name="rules"),
    url(r'^register/', views.register, name="register"),
    url(r'^login/', views.login, name="login"),
    url(r'^logout/', views.logout_view, name="logout"),
    url(r'^question/', views.question, name="questions"),

]
