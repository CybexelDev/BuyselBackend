# from django.core.management.base import BaseCommand
# from agents.models import AgentUserProfile


# class Command(BaseCommand):

#     help = "Synchronize expired agent subscriptions"

#     def handle(self, *args, **options):

#         count = 0
#         failed_count = 0

#         for agent in AgentUserProfile.objects.all().iterator():

#             try:
#                 agent.sync_subscription()
#                 count += 1

#             except Exception as error:
#                 failed_count += 1

#                 self.stderr.write(
#                     self.style.ERROR(
#                         f"Failed to synchronize agent "
#                         f"{agent.pk}: {error}"
#                     )
#                 )

#         self.stdout.write(
#             self.style.SUCCESS(
#                 f"Successfully synchronized {count} agents."
#             )
#         )

#         if failed_count:
#             self.stdout.write(
#                 self.style.WARNING(
#                     f"Failed to synchronize {failed_count} agents."
#                 )
#             )


from django.core.management.base import BaseCommand
from django.utils import timezone

from agents.models import AgentUserProfile
from developer.models import Subscription, ExpireAgents


class Command(BaseCommand):
    help = "Record agents whose subscriptions have all expired"

    def handle(self, *args, **options):
        today = timezone.localdate()
        now = timezone.now()

        checked_count = 0
        created_count = 0
        updated_count = 0
        skipped_count = 0
        failed_count = 0

        for agent in AgentUserProfile.objects.all().iterator():
            checked_count += 1

            try:
                subscriptions = Subscription.objects.filter(agent=agent)

                # No subscription history: do not create an expired record.
                if not subscriptions.exists():
                    skipped_count += 1
                    self.stdout.write(
                        f"[SKIPPED] {agent.username} - No subscription history"
                    )
                    continue

                # Any active subscription that has not ended?
                has_active_subscription = subscriptions.filter(
                    is_active=True,
                    end_date__gte=today,
                ).exists()

                if has_active_subscription:
                    skipped_count += 1
                    self.stdout.write(
                        f"[ACTIVE] {agent.username} - Subscription still active"
                    )
                    continue

                # Find the subscription that ended most recently.
                latest_subscription = subscriptions.order_by(
                    "-end_date", "-start_date"
                ).first()

                if latest_subscription is None:
                    skipped_count += 1
                    continue

                # Create or update the expired record with the latest
                # subscription that has ended.
                record, created = ExpireAgents.objects.get_or_create(
                    agent=agent,
                    defaults={
                        "subscription": latest_subscription,
                        "expired_on": now,
                        "reason": "All Subscriptions Expired",
                        "renewed": False,
                    },
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"[CREATED] {agent.username} | "
                            f"Latest subscription: {latest_subscription.plan_name} | "
                            f"End date: {latest_subscription.end_date}"
                        )
                    )
                else:
                    changed = False

                    if record.subscription_id != latest_subscription.pk:
                        record.subscription = latest_subscription
                        changed = True

                    if changed:
                        record.save(update_fields=["subscription"])
                        updated_count += 1
                        self.stdout.write(
                            f"[UPDATED] {agent.username} - Latest expired subscription linked"
                        )
                    else:
                        self.stdout.write(
                            f"[EXISTS] {agent.username} - Latest subscription already linked"
                        )

            except Exception as error:
                failed_count += 1
                self.stderr.write(
                    self.style.ERROR(
                        f"[FAILED] {agent.username}: {error}"
                    )
                )

        self.stdout.write("\n" + "=" * 42)
        self.stdout.write("AGENT SUBSCRIPTION EXPIRY SUMMARY")
        self.stdout.write("=" * 42)
        self.stdout.write(f"Agents checked       : {checked_count}")
        self.stdout.write(f"Records created      : {created_count}")
        self.stdout.write(f"Records updated      : {updated_count}")
        self.stdout.write(f"Agents skipped       : {skipped_count}")
        self.stdout.write(f"Failed               : {failed_count}")
        self.stdout.write("=" * 42)