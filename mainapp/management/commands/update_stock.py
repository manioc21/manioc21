from django.core.management.base import BaseCommand
from mainapp.apis import get_stock
from mainapp.models import Stock
from authenticate.models import User


class Command(BaseCommand):
    help = 'Update farmers'

    def handle(self, *args, **kwargs):
        fields = get_stock()
        for field in fields:
            try:
                coop,created = User.objects.get_or_create(username=field['coop'],coop=field['coop'])
                Stock.objects.get_or_create(coop=coop,data=field)
            except KeyError:
                self.stdout.write("key error")
        self.stdout.write("finished")