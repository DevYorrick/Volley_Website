from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.conf import settings
from django.template import loader
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage, send_mail
from .tokens import generate_token
import json
import re
from .models import *
from .forms import *
from volleyball import settings

# Create your tests here.
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

def signuptest(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        player_form = PlayerForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid() and player_form.is_valid():
            print('done')
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            player = player_form.save(commit=False)
            player.name = user.username
            player.save()

            auth_login(request, user)
            return redirect('home.html')  # Redirect to your home page
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        player_form = PlayerForm()

def logintest(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = authenticate(request, username=username)
            if user is not None:
                auth_login(request, user)
                return redirect('account')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

