from django.core.management.base import BaseCommand
from mainapp.apis import get_farmers
from mainapp.models import Coop

class Command(BaseCommand):
    help = 'Update coop'

    def handle(self, *args, **kwargs):
        farmers = get_farmers()
        coops = set([f['coop'] for f in farmers])
        for coop in coops:
            Coop.objects.get_or_create(name=coop)
        self.stdout.write("finished")