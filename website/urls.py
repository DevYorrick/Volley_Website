from . import views
from django.urls import path, include



urlpatterns = [
    path('home', views.home, name="home"),
    path('about', views.about, name="about"),
    path('attendance', views.attendance, name="attendance"),
    path('contact', views.contact, name="contact"),
    path('volleyball', views.volleyball, name="volleyball"),
    path('wednesday', views.wednesday, name="wednesday"),
    path('maps', views.maps, name="maps"),
    path("teams", views.teams, name="index"),
    path('<str:pk>/', views.DeletePlayer, name="deleteplayer"), 
]