from django.core.management.base import BaseCommand
from agents.models import AgentUserProfile


class Command(BaseCommand):

    help = "Synchronize expired agent subscriptions"

    def handle(self, *args, **options):

        count = 0

        for agent in AgentUserProfile.objects.all():

            agent.sync_subscription()
            count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully synchronized {count} agents."
            )
        )