from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from developer.models import Property


class Command(BaseCommand):

    help = (
        "Reduce property duration by one day and move expired "
        "properties to ExpiredProperty while checking active "
        "UserPlanSubscription."
    )

    # ==============================================================
    # SUBSCRIPTION ACTIVE CHECK
    # ==============================================================

    def is_subscription_active(self, subscription):

        """
        Check whether the property's UserPlanSubscription
        is currently active.

        This function intentionally checks the fields that are
        commonly used in subscription models.

        If your UserPlanSubscription has a specific status field,
        this can be adjusted exactly to that field.
        """

        if not subscription:

            return False

        # ----------------------------------------------------------
        # DEBUG: print subscription information
        # ----------------------------------------------------------

        self.stdout.write(
            self.style.NOTICE(
                "      Subscription found:"
            )
        )

        self.stdout.write(
            f"        ID: {subscription.pk}"
        )

        # ----------------------------------------------------------
        # Check is_active
        # ----------------------------------------------------------

        if hasattr(subscription, "is_active"):

            value = getattr(
                subscription,
                "is_active",
                False
            )

            self.stdout.write(
                f"        is_active: {value}"
            )

            if value is True:

                return True

        # ----------------------------------------------------------
        # Check status
        # ----------------------------------------------------------

        if hasattr(subscription, "status"):

            status = getattr(
                subscription,
                "status",
                None
            )

            self.stdout.write(
                f"        status: {status}"
            )

            if status:

                status_value = str(
                    status
                ).strip().lower()

                if status_value in [
                    "active",
                    "activated",
                    "paid",
                    "running",
                    "current",
                ]:

                    return True

        # ----------------------------------------------------------
        # Check plan_expiry_date
        # ----------------------------------------------------------

        if hasattr(
            subscription,
            "plan_expiry_date"
        ):

            expiry_date = getattr(
                subscription,
                "plan_expiry_date",
                None
            )

            self.stdout.write(
                f"        plan_expiry_date: "
                f"{expiry_date}"
            )

            if expiry_date:

                now = timezone.now()

                if expiry_date > now:

                    return True

        # ----------------------------------------------------------
        # Check expiry_date
        # ----------------------------------------------------------

        if hasattr(
            subscription,
            "expiry_date"
        ):

            expiry_date = getattr(
                subscription,
                "expiry_date",
                None
            )

            self.stdout.write(
                f"        expiry_date: "
                f"{expiry_date}"
            )

            if expiry_date:

                now = timezone.now()

                if expiry_date > now:

                    return True

        # ----------------------------------------------------------
        # No active indicator found
        # ----------------------------------------------------------

        self.stdout.write(
            self.style.WARNING(
                "        Subscription is NOT considered active."
            )
        )

        return False

    # ==============================================================
    # MAIN COMMAND
    # ==============================================================

    def handle(self, *args, **kwargs):

        self.stdout.write("")

        self.stdout.write(
            self.style.NOTICE(
                "=========================================="
            )
        )

        self.stdout.write(
            self.style.NOTICE(
                "PROPERTY EXPIRATION CHECK STARTED"
            )
        )

        self.stdout.write(
            self.style.NOTICE(
                "=========================================="
            )
        )

        self.stdout.write("")

        # ==========================================================
        # STEP 1
        # Reduce duration_days by one
        # ==========================================================

        self.stdout.write(
            self.style.NOTICE(
                "STEP 1: Reducing property durations..."
            )
        )

        updated_count = (
            Property.objects
            .filter(
                duration_days__gt=0
            )
            .update(
                duration_days=F("duration_days") - 1
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Durations updated: {updated_count}"
            )
        )

        self.stdout.write("")

        # ==========================================================
        # STEP 2
        # Get properties that reached zero
        # ==========================================================

        self.stdout.write(
            self.style.NOTICE(
                "STEP 2: Checking expired properties..."
            )
        )

        expired_property_ids = list(
            Property.objects
            .filter(
                duration_days__lte=0
            )
            .values_list(
                "id",
                flat=True
            )
        )

        if not expired_property_ids:

            self.stdout.write(
                self.style.SUCCESS(
                    "No properties reached expiration."
                )
            )

            return

        self.stdout.write(
            self.style.NOTICE(
                f"Found {len(expired_property_ids)} "
                f"properties with duration <= 0."
            )
        )

        self.stdout.write("")

        # ==========================================================
        # Counters
        # ==========================================================

        expired_count = 0
        active_subscription_count = 0
        no_subscription_count = 0
        inactive_subscription_count = 0
        skipped_count = 0
        failed_count = 0

        # ==========================================================
        # STEP 3
        # Process properties individually
        # ==========================================================

        for property_id in expired_property_ids:

            try:

                with transaction.atomic():

                    property_obj = (
                        Property.objects
                        .select_for_update()
                        .select_related(
                            "category",
                            "subcategory",
                            "purpose",
                            "user",
                            "package",
                            "subscription",
                            "single_property_package",
                        )
                        .prefetch_related(
                            "amenities",
                            "property_features__field",
                            "images",
                        )
                        .get(
                            pk=property_id
                        )
                    )

                    # ==================================================
                    # PROPERTY DEBUG INFORMATION
                    # ==================================================

                    self.stdout.write("")

                    self.stdout.write(
                        self.style.NOTICE(
                            "------------------------------------------"
                        )
                    )

                    self.stdout.write(
                        self.style.NOTICE(
                            "CHECKING PROPERTY"
                        )
                    )

                    self.stdout.write(
                        self.style.NOTICE(
                            "------------------------------------------"
                        )
                    )

                    self.stdout.write(
                        f"Property ID      : "
                        f"{property_obj.pk}"
                    )

                    self.stdout.write(
                        f"Property Code    : "
                        f"{property_obj.property_code}"
                    )

                    self.stdout.write(
                        f"Property Label   : "
                        f"{property_obj.label}"
                    )

                    self.stdout.write(
                        f"Duration Days    : "
                        f"{property_obj.duration_days}"
                    )

                    self.stdout.write(
                        f"User ID          : "
                        f"{property_obj.user_id}"
                    )

                    self.stdout.write(
                        f"Package ID       : "
                        f"{property_obj.package_id}"
                    )

                    self.stdout.write(
                        f"Subscription ID  : "
                        f"{property_obj.subscription_id}"
                    )

                    # ==================================================
                    # SAFETY CHECK
                    # ==================================================

                    if property_obj.duration_days > 0:

                        skipped_count += 1

                        self.stdout.write(
                            self.style.WARNING(
                                "SKIPPED"
                            )
                        )

                        self.stdout.write(
                            f"Duration is now "
                            f"{property_obj.duration_days}."
                        )

                        continue

                    # ==================================================
                    # CHECK USER PLAN SUBSCRIPTION
                    # ==================================================

                    subscription = (
                        property_obj.subscription
                    )

                    # --------------------------------------------------
                    # NO SUBSCRIPTION
                    # --------------------------------------------------

                    if not subscription:

                        no_subscription_count += 1

                        self.stdout.write(
                            self.style.WARNING(
                                "Subscription: NONE"
                            )
                        )

                        self.stdout.write(
                            self.style.NOTICE(
                                "Property will be expired."
                            )
                        )

                    # --------------------------------------------------
                    # SUBSCRIPTION EXISTS
                    # --------------------------------------------------

                    else:

                        is_active = (
                            self.is_subscription_active(
                                subscription
                            )
                        )

                        # ----------------------------------------------
                        # ACTIVE SUBSCRIPTION
                        # ----------------------------------------------

                        if is_active:

                            active_subscription_count += 1

                            self.stdout.write(
                                self.style.SUCCESS(
                                    "ACTIVE USER PLAN "
                                    "SUBSCRIPTION FOUND"
                                )
                            )

                            self.stdout.write(
                                self.style.SUCCESS(
                                    "Property will NOT be expired."
                                )
                            )

                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"Subscription ID: "
                                    f"{subscription.pk}"
                                )
                            )

                            continue

                        # ----------------------------------------------
                        # INACTIVE SUBSCRIPTION
                        # ----------------------------------------------

                        else:

                            inactive_subscription_count += 1

                            self.stdout.write(
                                self.style.WARNING(
                                    "Subscription exists "
                                    "but is NOT active."
                                )
                            )

                            self.stdout.write(
                                self.style.NOTICE(
                                    "Property will be expired."
                                )
                            )

                    # ==================================================
                    # EXPIRE PROPERTY
                    # ==================================================

                    property_code = (
                        property_obj.property_code
                    )

                    property_label = (
                        property_obj.label
                    )

                    self.stdout.write(
                        self.style.NOTICE(
                            "Moving property to "
                            "ExpiredProperty..."
                        )
                    )

                    # --------------------------------------------------
                    # This method:
                    #
                    # 1. Creates ExpiredProperty
                    # 2. Copies amenities
                    # 3. Copies features
                    # 4. Copies images
                    # 5. Deletes active Property
                    # --------------------------------------------------

                    property_obj.expire_property()

                    expired_count += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            "PROPERTY EXPIRED SUCCESSFULLY"
                        )
                    )

                    self.stdout.write(
                        f"Property: "
                        f"{property_label}"
                    )

                    self.stdout.write(
                        f"Code: "
                        f"{property_code}"
                    )

            # ======================================================
            # PROPERTY NO LONGER EXISTS
            # ======================================================

            except Property.DoesNotExist:

                skipped_count += 1

                self.stdout.write(
                    self.style.WARNING(
                        f"Property {property_id} "
                        f"does not exist."
                    )
                )

                self.stdout.write(
                    self.style.WARNING(
                        "It may already have been expired "
                        "by another process."
                    )
                )

                continue

            # ======================================================
            # OTHER ERROR
            # ======================================================

            except Exception as error:

                failed_count += 1

                self.stderr.write(
                    self.style.ERROR(
                        "ERROR WHILE PROCESSING PROPERTY"
                    )
                )

                self.stderr.write(
                    f"Property ID: {property_id}"
                )

                self.stderr.write(
                    f"Error: {error}"
                )

        # ==========================================================
        # FINAL SUMMARY
        # ==========================================================

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                "=========================================="
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "PROPERTY EXPIRATION SUMMARY"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "=========================================="
            )
        )

        self.stdout.write(
            f"Durations updated          : "
            f"{updated_count}"
        )

        self.stdout.write(
            f"Properties expired         : "
            f"{expired_count}"
        )

        self.stdout.write(
            f"Active subscription found  : "
            f"{active_subscription_count}"
        )

        self.stdout.write(
            f"No subscription            : "
            f"{no_subscription_count}"
        )

        self.stdout.write(
            f"Inactive subscription      : "
            f"{inactive_subscription_count}"
        )

        self.stdout.write(
            f"Skipped                    : "
            f"{skipped_count}"
        )

        self.stdout.write(
            f"Failed                     : "
            f"{failed_count}"
        )

        self.stdout.write(
            self.style.SUCCESS(
                "=========================================="
            )
        )

        # ==========================================================
        # FINAL STATUS
        # ==========================================================

        if failed_count:

            self.stdout.write(
                self.style.WARNING(
                    "Expiration check completed "
                    "with some failures."
                )
            )

        else:

            self.stdout.write(
                self.style.SUCCESS(
                    "Expiration check completed successfully."
                )
            )

        self.stdout.write("")