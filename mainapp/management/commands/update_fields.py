from django.core.management.base import BaseCommand
from mainapp.apis import get_fields
from mainapp.models import Field
from authenticate.models import User


class Command(BaseCommand):
    help = 'Update farmers'

    def handle(self, *args, **kwargs):
        fields = get_fields()
        for field in fields:
            try:
                coop,created = User.objects.get_or_create(username=field['coop'],coop=field['coop'])
                if created:
                    coop.set_password('admin')
                    coop.save()
                Field.objects.get_or_create(coop=coop,data=field)
            except KeyError:
                self.stdout.write("key error")
        self.stdout.write("finished")