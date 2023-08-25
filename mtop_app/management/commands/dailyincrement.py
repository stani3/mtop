from django.core.management.base import BaseCommand
from users.models import Profile
import schedule
import time
from datetime import datetime

def job():
    profiles = Profile.objects.filter(balance__gt=0)
    for profile in profiles:
        profile.increment_balance()
        profile.save()
        print(profile)
class Command(BaseCommand):

    def handle(self, *args, **options):
        schedule.every().day.at("00:00").do(job)
        try:
            while (True):
                now = datetime.now()
                if now.hour < 23 and now.hour != 0:
                    time.sleep((23-now.hour)*60*60)
                else:
                    time.sleep(600)
                schedule.run_pending()
        except:
            print("error")
