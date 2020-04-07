from django.core.management.base import BaseCommand
from mainapp.apis import *
from mainapp.models import *

def check_data(local_data,ona_data):
    ids = [data['_id'] for data in ona_data]
    for item in local_data:
        if item.data['_id'] not in ids:
            item.delete()
    return True


class Command(BaseCommand):
    help = 'Update pests'

    def handle(self, *args, **kwargs):
        #fields
        fields_ona = get_fields()
        fields_local = Field.objects.all()
        check_data(fields_local,fields_ona)
        self.stdout.write("finished fields")
        #farmers
        fields_ona = get_farmers()
        fields_local = Farmer.objects.all()
        check_data(fields_local,fields_ona)
        self.stdout.write("finished farmers")
        #pests
        fields_ona = get_pests()
        fields_local = Pest.objects.all()
        check_data(fields_local,fields_ona)
        self.stdout.write("finished pests")
        #sales
        fields_ona = get_sales()
        fields_local = Sales.objects.all()
        check_data(fields_local,fields_ona)
        self.stdout.write("finished sales")
        #stock
        fields_ona = get_stock()
        fields_local = Stock.objects.all()
        check_data(fields_local,fields_ona)
        self.stdout.write("finished stock")
        #supplies
        fields_ona = get_supplies()
        fields_local = Supply.objects.all()
        check_data(fields_local,fields_ona)
        self.stdout.write("finished supplies")
        #transformed products
        fields_ona = get_transformedproducts()
        fields_local = TransformedProduct.objects.all()
        check_data(fields_local,fields_ona)
        self.stdout.write("finished transformed products")