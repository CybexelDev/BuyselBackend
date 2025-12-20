from django.core.management.base import BaseCommand
from developer.models import Property, ExpiredProperty
from django.db import transaction
from collections import defaultdict
import re


class Command(BaseCommand):
    help = "Fix & generate property codes (remove hyphens, no duplicates)"

    @transaction.atomic
    def handle(self, *args, **kwargs):

        counters = defaultdict(int)

        def extract_number(code):
            """
            Extract trailing number from:
            KE-S-3, KES3, KESELL12 → 3, 3, 12
            """
            match = re.search(r"(\d+)$", code)
            return int(match.group(1)) if match else 0

        # ==================================================
        # STEP 1: CLEAN EXISTING CODES (REMOVE HYPHENS)
        # ==================================================
        for model in (Property, ExpiredProperty):
            for obj in model.objects.exclude(property_code__isnull=True):
                clean_code = obj.property_code.replace("-", "")
                if obj.property_code != clean_code:
                    obj.property_code = clean_code
                    obj.save(update_fields=["property_code"])

        # ==================================================
        # STEP 2: READ ALL EXISTING CODES (ACTIVE + EXPIRED)
        # ==================================================
        for model in (Property, ExpiredProperty):
            for p in model.objects.exclude(property_code__isnull=True):
                key = (p.state, p.purpose_id)
                counters[key] = max(
                    counters[key],
                    extract_number(p.property_code)
                )

        # ==================================================
        # STEP 3: GENERATE FOR ACTIVE PROPERTIES
        # ==================================================
        for prop in Property.objects.filter(property_code__isnull=True).order_by("id"):
            state = prop.state[:2].upper() if prop.state else "NA"
            purpose_letter = prop.purpose.name[0].upper()

            key = (prop.state, prop.purpose_id)
            counters[key] += 1

            prop.property_code = f"{state}{purpose_letter}{counters[key]}"
            prop.save(update_fields=["property_code"])

        # ==================================================
        # STEP 4: GENERATE FOR EXPIRED PROPERTIES
        # ==================================================
        for prop in ExpiredProperty.objects.filter(property_code__isnull=True).order_by("id"):
            state = prop.state[:2].upper() if prop.state else "NA"
            purpose_letter = prop.purpose.name[0].upper()

            key = (prop.state, prop.purpose_id)
            counters[key] += 1

            prop.property_code = f"{state}{purpose_letter}{counters[key]}"
            prop.save(update_fields=["property_code"])

        self.stdout.write(
            self.style.SUCCESS("✅ Property codes fixed: hyphens removed, no duplicates")
        )
