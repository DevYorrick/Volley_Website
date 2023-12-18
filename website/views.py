from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.conf import settings
from django.template import TemplateDoesNotExist, loader
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage, send_mail
from django.http import Http404, HttpResponseForbidden
from .tokens import generate_token
import json
import re
from .models import *
from .forms import *
from volleyball import settings

def is_staff_member(user):
    return user.is_staff

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
    pk = player.objects.get(id=id)

    if request.method =='POST':
        pk.delete()
        return redirect ('/wednesday/')

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
            return redirect('signup')

        if User.objects.filter(email=email):
            messages.error(request, "Email already in use")
            return redirect('signup')
        
        if len(username)>12:
            messages.error(request, "Username can't be more than 12 characters long")
            return redirect('signup')

        if password != password2:
            messages.error(request, "Passwords didn't match")
            return redirect('signup')

        if not username.isalnum():
            messages.error(request, "Username must be alpha numeric")
            return redirect('signup')

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False

        myuser.save()

        messages.success(request, "Your account has been created successfully, we have also send you a confirmation email, please confirm your email so you can use your account.")

        # Welcome Email
        subject = "Welcome to HAN Volleyball"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to the volleyball community \nThank you for using my website \nWe have also sent you a confirmation email, please confirm your email adress in order to activate your account \n\n Kind regards, Yorrick Reuser"
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
            # Get the selected_day from the form data
            selected_day = form.cleaned_data['selected_day']

            # Check if the user has already submitted attendance for the selected day
            existing_attendance = Attendance.objects.filter(user=request.user, selected_day=selected_day).first()

            if existing_attendance:
                # If an attendance record already exists, you can choose to reject the new submission or update the existing record.
                # For example, you might want to show a message to the user.
                messages.error(request, f"You have already submitted attendance for {selected_day}.")
            else:
                # Save the new attendance record
                attendance = form.save(commit=False)
                attendance.user = request.user
                attendance.save()
                messages.success(request, f"Attendance for {selected_day} recorded successfully.")
                return redirect('select_day')  # Redirect to your home page
    else:
        form = AttendanceForm()

    registered_days = Attendance.objects.filter(user=request.user).values_list('selected_day', flat=True)

    return render(request, 'select_day.html', {'form': form, 'registered_days': registered_days})

@login_required
def attendance_list(request, selected_day):
    attendances = Attendance.objects.all()
    attendees = Attendance.objects.filter(selected_day=selected_day)
    Monday = Attendance.objects.filter(selected_day="Monday")
    Monday_list = Monday[:42]
    Monday_waiting = Monday[42:]
    Wednesday = Attendance.objects.filter(selected_day="Wednesday")
    Wednesday_list = Wednesday[:28]
    Wednesday_waiting = Wednesday[28:]
    Friday = Attendance.objects.filter(selected_day="Friday")
    Friday_list = Friday[:28]
    Friday_waiting = Friday[28:]
    user_testing = User.objects.all()
    context = {
        'attendances': attendances,
        'attendance': attendance,
        'Monday': Monday,
        'Monday_list': Monday_list,
        'Monday_waiting': Monday_waiting,
        'attendees': attendees,
        'selected_day': selected_day,
        'Wednesday': Wednesday,
        'Wednesday_list': Wednesday_list,
        'Wednesday_waiting': Wednesday_waiting,
        'Friday_list': Friday_list,
        'Friday_waiting': Friday_waiting,
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
def create_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.user = request.user.username
            attendance.save()
            return render(request, 'success.html', {'user_instance': request.user, 'selected_day': attendance.selected_day})

    # If the form is not valid or it's a GET request, render the form again
    form = AttendanceForm()
    return render(request, 'select_day.html', {'form': form})

@login_required
def delete_attendance(request, attendance_id):
    # Get the Attendance object
    attendance = get_object_or_404(Attendance, id=attendance_id)

    # Check if the user has permission to delete this attendance
    if request.user == attendance.user:
        if request.method == 'POST':
            # If the request is a POST (confirmation), delete the attendance
            attendance.delete()
            messages.success(request, f"Attendance for {attendance.selected_day} deleted successfully.")
            return redirect('attendance_list', selected_day=attendance.selected_day)
    else:
        # If the user doesn't have permission, show an error message
        messages.error(request, "You do not have permission to delete this attendance.")
        return redirect('attendance_list', selected_day=attendance.selected_day)

    # If the request is not a POST, render the confirmation page
    return render(request, 'confirm_delete_attendance.html', {'attendance': attendance})

@login_required
def wednesday(request):
    players = player.objects.all()
    Friday = player.objects.filter(day="Friday")[:28]
    Wednesday = player.objects.filter(day="Wednesday")[:28]
    Monday = player.objects.filter(day="Monday")[0:0]
    name = UserProfile.objects.all()
    form = PlayerForm()

    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            # Get the user and selected day from the form
            user = request.user
            selected_day = form.cleaned_data['day']

            # Check if the user has already signed up for the selected day
            if player.objects.filter(name=user, day=selected_day).exists():
                messages.error(request, "You have already signed up for this day.")
            else:
                # Save the form if the user has not signed up for the selected day
                form.save()

        return redirect('wednesday_test')

    context = {'players': players, 'player': player, 'form': form, 'Wednesday': Wednesday, 'Monday': Monday,
               'Friday': Friday, 'name': name}
    return render(request, 'wednesday_test.html', context)

@login_required
@user_passes_test(is_staff_member)
def delete_all_attendance(request, selected_day):
    return render(request, 'confirm_delete_attendancelist.html', {'selected_day': selected_day})

@login_required
@user_passes_test(is_staff_member)
def confirm_delete_attendancelist(request, selected_day):
    if request.method == 'POST':
        # Perform the deletion here if confirmed
        Attendance.objects.filter(selected_day=selected_day).delete()
        messages.success(request, f"All {selected_day} attendees deleted successfully.")
        return redirect('attendance_list', selected_day=selected_day)

    return render(request, 'confirm_delete_attendancelist.html', {'selected_day': selected_day})