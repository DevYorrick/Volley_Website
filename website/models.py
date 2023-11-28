from django.db import models

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
    
   