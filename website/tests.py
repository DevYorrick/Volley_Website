"""
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

@login_required
def signup(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.user = request.user
            # Check if the user has already signed up for the selected day
            existing_attendance = Attendance.objects.filter(user=request.user, selected_day=attendance.selected_day)
            if not existing_attendance:
                attendance.save()
                return redirect('home')  # Redirect to your home page or wherever you want
            else:
                # Handle case where user is trying to sign up for the same day again
                # You can show a message or redirect them to a different page
                pass
    else:
        form = AttendanceForm()

    return render(request, 'signup.html', {'form': form})

@login_required
def wednesday_test(request):
    players = player.objects.all()
    Friday = player.objects.filter(day="Friday")[:28]
    Wednesday = player.objects.filter(day="Wednesday")[:28]
    Monday = player.objects.filter(day="Monday")[:42]

    form = PlayerForm(request.POST or None, initial={'user': request.user.username})

    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user.username  # Set the user before saving
            form.save()
            # Clear the form after submission
            form = PlayerForm(initial={'user': request.user.username})

    context = {'players': players, 'player': player, 'form': form, 'Wednesday': Wednesday, 'Monday': Monday,
                'Friday': Friday}
    return render(request, 'wednesday.html', context)
"""
"""
class PlayerForm(forms.ModelForm):
    user = forms.CharField(widget=forms.HiddenInput(), required=True)

    class Meta:
        model = player
        fields = ('user', 'day')

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.cleaned_data['user']
        if commit:
            instance.save()
        return instance

class player(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    Days = models.TextChoices("Days", "Monday Wednesday Friday")
    day = models.CharField(
        blank=False,
        choices=Days.choices,
        max_length=10,
        ) 
    def __str__(self):
        return f"{self.name} - {self.day} ({self.Days})"


@login_required
def attendance_list(request, selected_day):
    attendances = Attendance.objects.all()
    attendees = Attendance.objects.filter(selected_day=selected_day)
    Monday = Attendance.objects.filter(selected_day="Monday")[:42]
    Wednesday = Attendance.objects.filter(selected_day="Wednesday")[:28]
    Friday = Attendance.objects.filter(selected_day="Friday")[:28]
    user_testing = User.objects.all()
    print(f"Debug: Selected Day - {selected_day}")
    print(f"Debug: Attendees - {attendees.query}")  # Print the SQL query
    context = {
        'attendances': attendances,
        'attendance': attendance,
        'Monday': Monday,
        'attendees': attendees,
        'selected_day': selected_day,
        'Wednesday': Wednesday,
        'Friday': Friday,
    }

    # Determine the template name based on the selected_day
    template_name = f"{selected_day.lower()}.html"

    # Try to render the template, if it exists
    try:
        return render(request, template_name, context)
    except TemplateDoesNotExist:
        # If the template doesn't exist, render a default template or handle the case as needed
        return render(request, 'attendance_list.html', context)

        
@login_required
def select_day(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.user = request.user
            attendance.save()
            return redirect('select_day')  # Redirect to your home page
    else:
        form = AttendanceForm()

    return render(request, 'select_day.html', {'form': form})

@login_required
def wednesday(request):
    players = player.objects.all()
    Friday = player.objects.filter(day="Friday")[:28]
    Wednesday = player.objects.filter(day="Wednesday")[:28]
    Monday = player.objects.filter(day="Monday")[:42]
    form = PlayerForm()

    if request.method =='POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('wednesday')
    
    context = {'players': players, 'player': player, 'form': form, 'Wednesday' : Wednesday, 'Monday' : Monday, 'Friday' : Friday}
    return render(request, 'wednesday.html', context)

@login_required
def attendance_list(request, selected_day):
    attendances = Attendance.objects.all()
    attendees = Attendance.objects.filter(selected_day=selected_day)
    Monday = Attendance.objects.filter(selected_day="Monday")[:1]
    Wednesday = Attendance.objects.filter(selected_day="Wednesday")[:28]
    Friday = Attendance.objects.filter(selected_day="Friday")[:28]
    user_testing = User.objects.all()
    context = {
        'attendances': attendances,
        'attendance': attendance,
        'Monday': Monday,
        'attendees': attendees,
        'selected_day': selected_day,
        'Wednesday': Wednesday,
        'Friday': Friday,
    }

    # Determine the template name based on the selected_day
    template_name = f"{selected_day.lower()}.html"

    # Try to render the template, if it exists
    try:
        return render(request, template_name, context)
    except TemplateDoesNotExist:
        # If the template doesn't exist, render a default template or handle the case as needed
        return render(request, 'attendance_list.html', context)

"""