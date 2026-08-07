from django.core.management.base import BaseCommand

from developer.views import sync_agent_property_statuses


class Command(BaseCommand):
    help = "Sync agent property expiry and restoration statuses."

    def handle(self, *args, **options):
        result = sync_agent_property_statuses()

        self.stdout.write(
            self.style.SUCCESS(
                (
                    "Agent property expiry sync completed. "
                    f"Expired: {result['expired']}, "
                    f"Restored: {result['restored']}."
                )
            )
        )