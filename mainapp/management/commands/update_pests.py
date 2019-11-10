from django.core.management.base import BaseCommand
from mainapp.apis import get_pests
from mainapp.models import Pest
from authenticate.models import User


class Command(BaseCommand):
    help = 'Update pests'

    def handle(self, *args, **kwargs):
        fields = get_pests()
        for field in fields:
            try:
                coop,created = User.objects.get_or_create(username=field['coop'],coop=field['coop'])
                if created:
                    coop.set_password('admin')
                    coop.save()
                Pest.objects.get_or_create(coop=coop,data=field)
            except KeyError:
                self.stdout.write("key error")
        self.stdout.write("finished")