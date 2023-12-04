import os
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "volleyball.settings")
django.setup()

from website.models import Attendance

attendees = Attendance.objects.filter(selected_day='monday')
print(attendees)