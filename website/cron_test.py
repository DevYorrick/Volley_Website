"""
website/cron.py
from django_cron import CronJobBase, Schedule
from .models import Attendance
import random

class DeleteMondayUsersCronJob(CronJobBase):
    print("Cron job started")
    RUN_EVERY_MINS = 1  # once a day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'website.delete_monday_users_cron_job'
    
    def do(self):
        print('Deleting users who signed up for Monday...')
        try:
            # Your logic to delete users for Monday goes here
            Attendance.objects.filter(selected_day='Monday').delete()
            print('Deletion completed successfully.')
        except Exception as e:
            print(f'Error during deletion: {e}')

website/urls.py    
from django_cron import CronJobBase, Schedule
from .cron import DeleteMondayUsersCronJob

class DeleteMondayUsersCronJob(CronJobBase):
    print("Cron job still goingash")
    RUN_EVERY_MINS = 1  # adjust as needed
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'website.delete_monday_users_cron_job'  # must be unique within your project

    def do(self):
        from website.cron import delete_monday_users
        delete_monday_users()

volleyball/settings.py

installes apps:
    'django_cron',

CRON_CLASSES = [
    'website.cron.DeleteMondayUsersCronJob',
]
DJANGO_CRON_OVERRIDE = True
"""