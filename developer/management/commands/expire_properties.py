from django.core.management.base import BaseCommand
from django.db.models import F

from developer.models import Property


class Command(BaseCommand):
    help = "Reduce property duration and move expired properties"

    def handle(self, *args, **kwargs):

        # ------------------------------------
        # Reduce duration_days by 1
        # ------------------------------------
        Property.objects.filter(
            duration_days__gt=0
        ).update(
            duration_days=F("duration_days") - 1
        )

        # ------------------------------------
        # Move expired properties
        # ------------------------------------
        expired_count = 0

        for property_obj in Property.objects.filter(duration_days=0):

            property_obj.save()   # Property.save() moves it to ExpiredProperty

            expired_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"{expired_count} properties moved to ExpiredProperty."
            )
        )