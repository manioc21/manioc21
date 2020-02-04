from django.core.management.base import BaseCommand
from mainapp.models import *


class Command(BaseCommand):
    help = 'Update pests'

    def handle(self, *args, **kwargs):
        #fields
        fields_local = Field.objects.all()
        for field in fields_local:
            field.history = True
            field.save()
        self.stdout.write("finished fields")
        #farmers
        fields_local = Farmer.objects.all()
        for field in fields_local:
            field.history = True
            field.save()
        self.stdout.write("finished farmers")
        #pests
        fields_local = Pest.objects.all()
        for field in fields_local:
            field.history = True
            field.save()
        self.stdout.write("finished pests")
        #sales
        fields_local = Sales.objects.all()
        for field in fields_local:
            field.history = True
            field.save()
        self.stdout.write("finished sales")
        #stock
        fields_local = Stock.objects.all()
        for field in fields_local:
            field.history = True
            field.save()
        self.stdout.write("finished stock")
        #supplies
        fields_local = Supply.objects.all()
        for field in fields_local:
            field.history = True
            field.save()
        self.stdout.write("finished supplies")
        #transformed products
        fields_local = TransformedProduct.objects.all()
        for field in fields_local:
            field.history = True
            field.save()
        self.stdout.write("finished transformed products")
        #payments
        fields_local = Payment.objects.all()
        for field in fields_local:
            field.history = True
            field.save()
        self.stdout.write("finished payments")