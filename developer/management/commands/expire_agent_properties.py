# from django.core.management.base import BaseCommand

# from agents.models import AgentProperty


# class Command(BaseCommand):

#     help = (
#         "Reduce AgentProperty duration every day. "
#         "Active subscriptions protect properties from expiry. "
#         "When duration reaches zero and there is no active subscription, "
#         "move the property to ExpiredAgentProperty."
#     )

#     def handle(self, *args, **kwargs):

#         self.stdout.write("")
#         self.stdout.write(
#             self.style.WARNING(
#                 "=========================================="
#             )
#         )
#         self.stdout.write(
#             self.style.WARNING(
#                 "AGENT PROPERTY EXPIRY CHECK STARTED"
#             )
#         )
#         self.stdout.write(
#             self.style.WARNING(
#                 "=========================================="
#             )
#         )

#         checked_count = 0
#         active_subscription_count = 0
#         duration_reduced_count = 0
#         expired_count = 0
#         failed_count = 0

#         properties = (
#             AgentProperty.objects
#             .select_related(
#                 "agent",
#                 "category",
#                 "subcategory",
#                 "purpose",
#                 "subscription",
#             )
#             .prefetch_related(
#                 "amenities",
#                 "field_values",
#                 "images",
#                 "selling_points",
#                 "landmarks",
#             )
#         )

#         for property_obj in properties:

#             checked_count += 1

#             try:

#                 # ==================================================
#                 # CHECK ACTIVE SUBSCRIPTION
#                 # ==================================================

#                 has_active_subscription = (
#                     property_obj.has_active_subscription()
#                 )

#                 # ==================================================
#                 # REDUCE DURATION EVERY DAY
#                 # ==================================================

#                 if property_obj.duration_days > 0:

#                     old_duration = property_obj.duration_days

#                     property_obj.duration_days -= 1

#                     property_obj.save(
#                         update_fields=[
#                             "duration_days"
#                         ]
#                     )

#                     duration_reduced_count += 1

#                     self.stdout.write(
#                         self.style.SUCCESS(
#                             f"[DURATION] "
#                             f"Property {property_obj.pk}: "
#                             f"{old_duration} -> "
#                             f"{property_obj.duration_days}"
#                         )
#                     )

#                 # ==================================================
#                 # ACTIVE SUBSCRIPTION
#                 # ==================================================

#                 if has_active_subscription:

#                     active_subscription_count += 1

#                     self.stdout.write(
#                         self.style.SUCCESS(
#                             f"[ACTIVE PLAN] "
#                             f"Property {property_obj.pk} "
#                             f"kept active. "
#                             f"duration={property_obj.duration_days}"
#                         )
#                     )

#                     # IMPORTANT:
#                     #
#                     # Even if duration_days == 0,
#                     # active subscription protects the property.
#                     #
#                     continue

#                 # ==================================================
#                 # NO ACTIVE SUBSCRIPTION
#                 # ==================================================

#                 if property_obj.duration_days <= 0:

#                     self.stdout.write(
#                         self.style.WARNING(
#                             f"[EXPIRED] "
#                             f"Property {property_obj.pk} "
#                             f"has no active subscription and "
#                             f"duration={property_obj.duration_days}"
#                         )
#                     )

#                     expired_property = (
#                         property_obj.move_to_expired()
#                     )

#                     if expired_property:

#                         expired_count += 1

#                         self.stdout.write(
#                             self.style.SUCCESS(
#                                 f"Property {property_obj.pk} "
#                                 f"moved to ExpiredAgentProperty."
#                             )
#                         )

#             except Exception as error:

#                 failed_count += 1

#                 self.stdout.write(
#                     self.style.ERROR(
#                         f"[ERROR] "
#                         f"Property "
#                         f"{getattr(property_obj, 'pk', 'UNKNOWN')}: "
#                         f"{error}"
#                     )
#                 )

#         # ==========================================================
#         # FINAL REPORT
#         # ==========================================================

#         self.stdout.write("")

#         self.stdout.write(
#             self.style.WARNING(
#                 "=========================================="
#             )
#         )

#         self.stdout.write(
#             self.style.SUCCESS(
#                 "AGENT PROPERTY EXPIRY CHECK COMPLETED"
#             )
#         )

#         self.stdout.write(
#             f"Total checked        : {checked_count}"
#         )

#         self.stdout.write(
#             f"Active subscription  : {active_subscription_count}"
#         )

#         self.stdout.write(
#             f"Duration reduced     : {duration_reduced_count}"
#         )

#         self.stdout.write(
#             f"Moved to expired     : {expired_count}"
#         )

#         self.stdout.write(
#             f"Failed               : {failed_count}"
#         )

#         self.stdout.write(
#             self.style.WARNING(
#                 "=========================================="
#             )
#         )





from django.core.management.base import BaseCommand

from agents.models import AgentProperty


class Command(BaseCommand):

    help = (
        "Reduce AgentProperty duration daily and move properties "
        "to ExpiredAgentProperty when there is no active plan "
        "and duration reaches zero."
    )

    def handle(self, *args, **kwargs):

        self.stdout.write("")
        self.stdout.write(
            self.style.WARNING(
                "=========================================="
            )
        )
        self.stdout.write(
            self.style.WARNING(
                "AGENT PROPERTY EXPIRY CHECK STARTED"
            )
        )
        self.stdout.write(
            self.style.WARNING(
                "=========================================="
            )
        )

        checked_count = 0
        active_subscription_count = 0
        duration_reduced_count = 0
        expired_count = 0
        failed_count = 0

        properties = (
            AgentProperty.objects
            .select_related(
                "agent",
                "category",
                "subcategory",
                "purpose",
                "subscription",
            )
            .prefetch_related(
                "amenities",
                "field_values",
                "images",
                "selling_points",
                "landmarks",
            )
        )

        for property_obj in properties:

            checked_count += 1

            try:

                # ==========================================
                # CHECK ACTIVE SUBSCRIPTION
                # ==========================================

                has_active_subscription = (
                    property_obj.has_active_subscription()
                )

                # ==========================================
                # ACTIVE PLAN
                # ==========================================

                if has_active_subscription:

                    active_subscription_count += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"[ACTIVE PLAN] "
                            f"Property {property_obj.pk} "
                            f"kept active. "
                            f"duration={property_obj.duration_days}"
                        )
                    )

                    # Active plan protects property
                    continue

                # ==========================================
                # NO ACTIVE PLAN
                # ==========================================

                if property_obj.duration_days > 0:

                    old_duration = property_obj.duration_days

                    property_obj.duration_days -= 1

                    property_obj.save(
                        update_fields=["duration_days"]
                    )

                    duration_reduced_count += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"[DURATION] "
                            f"Property {property_obj.pk}: "
                            f"{old_duration} -> "
                            f"{property_obj.duration_days}"
                        )
                    )

                # ==========================================
                # CHECK EXPIRY
                # ==========================================

                if property_obj.duration_days <= 0:

                    self.stdout.write(
                        self.style.WARNING(
                            f"[EXPIRED] "
                            f"Property {property_obj.pk} "
                            f"has no active subscription "
                            f"and duration={property_obj.duration_days}"
                        )
                    )

                    expired_property = (
                        property_obj.move_to_expired()
                    )

                    if expired_property:

                        expired_count += 1

                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Property {property_obj.pk} "
                                f"moved to ExpiredAgentProperty."
                            )
                        )

            except Exception as error:

                failed_count += 1

                self.stdout.write(
                    self.style.ERROR(
                        f"[ERROR] "
                        f"Property "
                        f"{getattr(property_obj, 'pk', 'UNKNOWN')}: "
                        f"{error}"
                    )
                )

        # ==========================================
        # FINAL REPORT
        # ==========================================

        self.stdout.write("")

        self.stdout.write(
            self.style.WARNING(
                "=========================================="
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "AGENT PROPERTY EXPIRY CHECK COMPLETED"
            )
        )

        self.stdout.write(
            f"Total checked        : {checked_count}"
        )

        self.stdout.write(
            f"Active subscription  : {active_subscription_count}"
        )

        self.stdout.write(
            f"Duration reduced     : {duration_reduced_count}"
        )

        self.stdout.write(
            f"Moved to expired     : {expired_count}"
        )

        self.stdout.write(
            f"Failed               : {failed_count}"
        )

        self.stdout.write(
            self.style.WARNING(
                "=========================================="
            )
        )