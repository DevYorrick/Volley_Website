from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class player(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        )
    Days = models.TextChoices("Days", "Monday Wednesday")
    day = models.CharField(
        blank=False,
        choices=Days.choices,
        max_length=10,
        ) 
    def __str__(self):
        return self.name, self.day, self.Days, self.id
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    #profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day_choices = [('Monday', 'Monday'), ('Wednesday', 'Wednesday'), ('Friday', 'Friday')]
    selected_day = models.CharField(max_length=10, choices=day_choices)

    def __str__(self):
        return f"{self.user.username} - {self.selected_day}"