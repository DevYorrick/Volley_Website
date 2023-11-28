from django.shortcuts import render, redirect
import json
from django.conf import settings
from django.template import loader
import re
from django.utils.timezone import datetime
from django.http import HttpResponse
from .models import *
from .forms import *



def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def attendance(request):
    return render(request, 'attendance.html')

def monday(request):
    return render(request, 'monday.html')

def contact(request):
    return render(request, 'contact.html')

def volleyball(request):
    return render(request, 'volleyball.html')

def index(request):
    return render(request, 'test.html')

def maps(request):
    return render(request, 'maps.html')

def wednesday(request):
    players = player.objects.all()
    Wednesday = player.objects.filter(day="Wednesday")
    Monday = player.objects.filter(day="Monday")
    form = playerForm()
    if request.method =='POST':
        form = playerForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/wednesday')
    
    context = {'players': players, 'player': player, 'form': form, 'Wednesday' : Wednesday, 'Monday' : Monday}
    return render(request, 'wednesday.html', context)

def teams(request):
    template = loader.get_template('teams.html')
    context = {
        'team1': get_teams4("Yorrick", "Canray", "Vladdy", "Antonia", "Albert", "Karim"),
        'team2': get_teams5("Jeroen", "Benas", "Remo", "Tom", "Yannis", "Zain"),
        'team3': get_teams6("Luba", "Anne", "Maaike", "Neda", "Ghiz", "Steph"),
        'title': 'Volleybal'}
    return HttpResponse(template.render(context, request))

def get_teams4(first, second, third, fourth, fifth, sixth):
    return [first, second, third, fourth, fifth, sixth]

def get_teams5(first, second, third, fourth, fifth, sixth):
    return [first, second, third, fourth, fifth, sixth]

def get_teams6(first, second, third, fourth, fifth, sixth):
    return [first, second, third, fourth, fifth, sixth]

def DeletePlayer(request, pk):
    pk = player.objects.get(id=pk)

    if request.method =='POST':
        pk.delete()
        return redirect ('/wednesday')

    context = {'pk': pk}
    return render(request, 'delete_player.html', context)



