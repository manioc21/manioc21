from django.core.management.base import BaseCommand
from mainapp.apis import get_transformedproducts
from mainapp.models import TransformedProduct
from authenticate.models import User


class Command(BaseCommand):
    help = 'Update transformed products'

    def handle(self, *args, **kwargs):
        fields = get_transformedproducts()
        for field in fields:
            try:
                coop,created = User.objects.get_or_create(username=field['coop'],coop=field['coop'])
                if created:
                    coop.set_password('admin')
                    coop.save()
                TransformedProduct.objects.get_or_create(coop=coop,data=field)
            except KeyError:
                self.stdout.write("key error")
        self.stdout.write("finished")