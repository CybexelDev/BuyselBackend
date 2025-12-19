from django.core.management.base import BaseCommand
from django.db.models import F
from developer.models import Property, Premium, Agents

class Command(BaseCommand):
    help = "Reduce duration_days daily and move expired items for Property, Premium, and Agents"

    def handle(self, *args, **kwargs):
        # -----------------------------
        # 1️⃣ Reduce duration safely
        # -----------------------------
        Property.objects.filter(duration_days__gt=0).update(
            duration_days=F('duration_days') - 1
        )

        Premium.objects.filter(duration_days__gt=0).update(
            duration_days=F('duration_days') - 1
        )

        Agents.objects.filter(duration_days__gt=0).update(
            duration_days=F('duration_days') - 1
        )

        # -----------------------------
        # 2️⃣ Trigger expiry move
        # -----------------------------
        for prop in Property.objects.filter(duration_days__lte=0):
            prop.save()  # Moves to ExpiredProperty

        for premium in Premium.objects.filter(duration_days__lte=0):
            premium.save()  # Moves to ExpiredPremium

        for agent in Agents.objects.filter(duration_days__lte=0):
            agent.save()  # Moves to ExpireAgents

        self.stdout.write(
            self.style.SUCCESS("Durations reduced and expired items moved for all models")
        )
