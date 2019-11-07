from django.core.management.base import BaseCommand
from mainapp.apis import get_supplies
from mainapp.models import Supply
from authenticate.models import User


class Command(BaseCommand):
    help = 'Update supplies'

    def handle(self, *args, **kwargs):
        fields = get_supplies()
        for field in fields:
            try:
                coop,created = User.objects.get_or_create(username=field['coop'],coop=field['coop'])
                Supply.objects.get_or_create(coop=coop,data=field)
            except KeyError:
                self.stdout.write("key error")
        self.stdout.write("finished")