from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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
    form = PlayerForm()
    if request.method =='POST':
        form = PlayerForm(request.POST)
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

def DeletePlayer(request, id):
    pk = player.objects.get(id=pk)

    if request.method =='POST':
        pk.delete()
        return redirect ('/wednesday')

    context = {'pk': pk}
    return render(request, 'delete_player.html', context)

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "Email already in use")
            return redirect('home')
        
        if len(username)>12:
            messages.error(request, "Username can't be more than 12 characters long")
            return redirect('home')

        if password != password2:
            messages.error(request, "Passwords didn't match")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Username must be alpha numeric")
            return redirect('home')

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False

        myuser.save()

        messages.success(request, "Your account has been created successfully, we have also send you a confirmation email, please confirm your email so you can use your account.")

        # Welcome Email
        subject = "Welcome to HAN Volleyball"
        message = "Hello" + myuser.first_name + "!! \n" + "Welcome to the volleyball community \n Thank you for using my website \n We have also sent you a confirmation email, please confirm your email adress in order to activate your account \n\n Kind regards, Yorrick Reuser"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email adress confirmation email

        current_site = get_current_site(request)
        email_subject = "Confirmation your email @ HAN ISB Volleyball"
        message2 = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('login')
    
    return render(request, "signup.html")

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            fname = user.first_name
            return render(request, "account.html", {'fname': fname})
        
        else:
            messages.error(request, "Incorrect log in information")
            return redirect('home')
    return render(request, 'login.html')

def account(request):
    return render(request, 'account.html')

def select_day(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.user = request.user
            attendance.save()
            return redirect('home')  # Redirect to your home page
    else:
        form = AttendanceForm()

    return render(request, 'select_day.html', {'form': form})

def user_logout(request):
    auth_logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
    
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        auth_login(request, myuser)
        return redirect ('home')
    else:
        return render(request, 'activation_failed.html')
    
@login_required
def delete_account(request):
    if request.method == 'POST':
        # Delete the user account and log them out
        request.user.delete()
        auth_logout(request)
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home')

    return render(request, 'delete_account.html')

@login_required
def select_day(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.user = request.user
            attendance.save()
            return redirect('home')  # Redirect to your home page
    else:
        form = AttendanceForm()

    return render(request, 'select_day.html', {'form': form})

@login_required
def attendance_list(request, selected_day):
    attendees = Attendance.objects.filter(selected_day=selected_day)
    print(f"Debug: Selected Day - {selected_day}")
    print(f"Debug: Attendees - {attendees.query}")  # Print the SQL query
    return render(request, 'attendance_list.html', {'attendees': attendees, 'selected_day': selected_day})

@login_required
def create_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.user = request.user
            attendance.save()
            return render(request, 'success.html', {'user_instance': request.user, 'selected_day': attendance.selected_day})

    # If the form is not valid or it's a GET request, render the form again
    form = AttendanceForm()
    return render(request, 'select_day.html', {'form': form})