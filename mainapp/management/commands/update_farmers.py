from django.core.management.base import BaseCommand
from mainapp.apis import get_farmers
from mainapp.models import Farmer
from authenticate.models import User


class Command(BaseCommand):
    help = 'Update farmers'

    def handle(self, *args, **kwargs):
        farmers = get_farmers()
        for farmer in farmers:
            try:
                coop,created = User.objects.get_or_create(username=farmer['coop'],coop=farmer['coop'])
                Farmer.objects.get_or_create(coop=coop,data=farmer)
            except KeyError:
                self.stdout.write("key error")
        self.stdout.write("finished")