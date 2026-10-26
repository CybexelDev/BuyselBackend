from django.core.management.base import BaseCommand
from developer.models import Property, ExpiredProperty
from django.db import transaction
from collections import defaultdict
import re

class Command(BaseCommand):
    help = "Fix & generate property codes (remove hyphens, no duplicates) for all properties"

    @transaction.atomic
    def handle(self, *args, **kwargs):

        counters = defaultdict(int)

        def extract_number(code):
            
            match = re.search(r"(\d+)$", code)
            return int(match.group(1)) if match else 0

        # Combine both models into a single list
        all_models = [Property, ExpiredProperty]

        for model in all_models:
            for obj in model.objects.exclude(property_code__isnull=True):
                clean_code = obj.property_code.replace("-", "")
                if obj.property_code != clean_code:
                    obj.property_code = clean_code
                    obj.save(update_fields=["property_code"])

        for model in all_models:
            for obj in model.objects.exclude(property_code__isnull=True):
                state_prefix = (obj.state[:2].upper() if obj.state else "NA")
                purpose_letter = obj.purpose.name[0].upper()
                key = (state_prefix, purpose_letter)
                counters[key] = max(
                    counters[key],
                    extract_number(obj.property_code)
                )

        for model in all_models:
            for obj in model.objects.filter(property_code__isnull=True).order_by("id"):
                state_prefix = obj.state[:2].upper() if obj.state else "NA"
                purpose_letter = obj.purpose.name[0].upper()

                key = (state_prefix, purpose_letter)
                counters[key] += 1

                obj.property_code = f"{state_prefix}{purpose_letter}{counters[key]}"
                obj.save(update_fields=["property_code"])

        self.stdout.write(
            self.style.SUCCESS("✅ Property codes fixed for all properties: hyphens removed, no duplicates")
        )
