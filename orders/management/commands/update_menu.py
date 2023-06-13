import logging

from django.core.management import BaseCommand

from data.menu import MENU
from orders.models import MenuItem

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Reads menu from data files and upserts them into the database"

    def handle(self, *args, **options):
        for index, (code, data) in enumerate(MENU):
            print(code)
            MenuItem.objects.update_or_create(
                code=code,
                defaults={**data}#, "index": index}
            )

        MenuItem.objects.exclude(code__in=[code for code, _ in MENU]).delete()

        self.stdout.write("Done 🥙")
