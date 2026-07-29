import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bysel.settings")  # Replace with your settings module

import django
django.setup()

from django.core.management import call_command

with open("backup.json", "w", encoding="utf-8") as f:
    call_command(
        "dumpdata",
        exclude=["auth.permission", "contenttypes"],
        indent=2,
        stdout=f,
    )

print("✅ Backup completed successfully.")