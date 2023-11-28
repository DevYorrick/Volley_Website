from django import forms 
from django.forms import ModelForm

from .models import *

class playerForm(forms.ModelForm):
    
    class Meta:
        model = player
        fields = '__all__'