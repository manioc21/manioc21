from django.core.management.base import BaseCommand
from mainapp.apis import get_sales
from mainapp.models import Sales
from authenticate.models import User


class Command(BaseCommand):
    help = 'Update farmers'

    def handle(self, *args, **kwargs):
        fields = get_sales()
        for field in fields:
            try:
                coop,created = User.objects.get_or_create(username=field['coop'],coop=field['coop'])
                Sales.objects.get_or_create(coop=coop,data=field)
            except KeyError:
                self.stdout.write("key error")
        self.stdout.write("finished")