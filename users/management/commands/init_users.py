import logging
from datetime import datetime

from django.core.management import BaseCommand

from users.models import User

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Init users"

    def handle(self, *args, **options):
        users = User.objects.get_or_create(chat_id=155493213, username="бездонный желужок", phone="+995995995995")
        self.stdout.write("Done 🥙")
