from django.core.management.base import BaseCommand, CommandError
from homepage.models import Event
from django.utils import timezone

class Command(BaseCommand):
    help = 'does this say anything'
    def handle(self, *args, **options): ##what do these arguments mean?
        EventTime = Event.objects.all()
        for LateEvents in EventTime:
                ##if timezone.now().day > LateEvents.date.day: ##only delete events that have passed for more than 1 day (keep 1 day events) ##this doesnt work comparing days
                if timezone.now() > LateEvents.date: ##if todays datetime already passed an event's datetime
                        self.stdout.write(str(LateEvents.date))
                        Event.objects.filter(date=LateEvents.date).delete()



