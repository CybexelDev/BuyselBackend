from django.core.management.base import BaseCommand
from django.db.models import F

from developer.models import Property

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import F

# Change this import according to your app name
from developer.models import Property


class Command(BaseCommand):
    help = "Reduce property duration and move expired properties"

    def handle(self, *args, **kwargs):

        # --------------------------------------------------
        # Reduce duration_days by one
        # --------------------------------------------------

        updated_count = (
            Property.objects
            .filter(duration_days__gt=0)
            .update(
                duration_days=F("duration_days") - 1
            )
        )

        self.stdout.write(
            f"{updated_count} property durations updated."
        )

        # --------------------------------------------------
        # Get properties whose duration reached zero
        # --------------------------------------------------

        expired_property_ids = list(
            Property.objects
            .filter(duration_days__lte=0)
            .values_list("id", flat=True)
        )

        expired_count = 0
        failed_count = 0

        # --------------------------------------------------
        # Move each property safely
        # --------------------------------------------------

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
                        .get(id=property_id)
                    )

                    # Another process may already have changed it
                    if property_obj.duration_days > 0:
                        continue

                    # This method creates ExpiredProperty,
                    # copies amenities, features and images,
                    # then deletes the active Property.
                    property_obj.expire_property()

                    expired_count += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Expired property moved: "
                            f"{property_obj.label}"
                        )
                    )

            except Property.DoesNotExist:

                # Property may already have been moved
                continue

            except Exception as error:

                failed_count += 1

                self.stderr.write(
                    self.style.ERROR(
                        f"Failed to expire property "
                        f"{property_id}: {error}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"{expired_count} properties moved "
                f"to ExpiredProperty."
            )
        )

        if failed_count:

            self.stdout.write(
                self.style.WARNING(
                    f"{failed_count} properties failed."
                )
            )