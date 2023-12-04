from django import forms 
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class PlayerForm(forms.ModelForm):
    class Meta:
        model = player
        fields = ('name', 'day')

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number']  # Add additional fields as needed, 'profile_picture'

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    name = forms.CharField(max_length=100, required=True, help_text='Required. Enter your full name.')

    class Meta:
        model = User
        fields = ('username', 'name', 'email')

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username')

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['selected_day']