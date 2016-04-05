from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about-us/', views.about_us, name='about_us'),
    url(r'^leader-board/', views.leader_board, name="leader_board"),
    url(r'^rules/', views.rules, name="rules"),    
]