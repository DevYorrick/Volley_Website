import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from website.models import Attendance

class Command(BaseCommand):
    help = 'Delete Monday attendance records'

    def handle(self, *args, **options):
        # Check if today is Tuesday
        today = datetime.now().date()
        if today.weekday() != 1:  # Tuesday corresponds to index 1
            self.stdout.write(self.style.SUCCESS('Not Tuesday. No action needed.'))
            return

        # Generate a random time during the day
        random_hour = random.randint(0, 23)
        random_minute = random.randint(0, 59)
        scheduled_time = datetime(today.year, today.month, today.day, random_hour, random_minute)

        # Check if the current time is after the scheduled time
        if datetime.now() < scheduled_time:
            self.stdout.write(self.style.SUCCESS('Not yet time. No action needed.'))
            return

        # Delete Monday attendance records
        Attendance.objects.filter(selected_day='Monday').delete()
        self.stdout.write(self.style.SUCCESS('Monday attendance records deleted successfully.'))