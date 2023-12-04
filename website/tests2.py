from .models import Attendance

attendees = Attendance.objects.filter(selected_day='monday')
print(attendees)