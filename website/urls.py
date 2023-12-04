from . import views
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('home', views.home, name="home"),
    path('', views.home, name="home"),
    path('signup', views.signup, name='signup'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('success', views.create_attendance, name='success'),
    path('account', views.account, name='account'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('select_day', views.select_day, name='select_day'),
    path('attendance_list/<str:selected_day>/', views.attendance_list, name='attendance_list'),
    path('about', views.about, name="about"),
    path('attendance', views.attendance, name="attendance"),
    path('contact', views.contact, name="contact"),
    path('volleyball', views.volleyball, name="volleyball"),
    path('monday', views.monday, name="monday"),
    path('wednesday/', views.wednesday, name="wednesday"),
    path('<int:id>/', views.DeletePlayer, name='delete_player'),
    path('maps', views.maps, name="maps"),
    path('delete_account/', views.delete_account, name='delete_account'),
]