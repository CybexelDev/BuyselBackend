from django.core.management.base import BaseCommand
from developer.models import Property, Premium

class Command(BaseCommand):
    help = "Reduce duration_days daily for Property and Premium"

    def handle(self, *args, **kwargs):

        # ---------- PROPERTY ----------
        for prop in Property.objects.filter(duration_days__gt=0):
            prop.duration_days -= 1
            prop.save()

        # ---------- PREMIUM ----------
        for premium in Premium.objects.filter(duration_days__gt=0):
            premium.duration_days -= 1
            premium.save()

        self.stdout.write(self.style.SUCCESS("Durations reduced successfully"))
