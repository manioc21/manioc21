from django.core.management.base import BaseCommand
from mainapp.models import Field
import datetime

class Command(BaseCommand):
    help = 'Check harvest'

    def handle(self, *args, **kwargs):
        today = str(datetime.date.today())
        fields = Field.objects.filter(data__harvestdate__lte=today,status='not_ready')
        for field in fields:
        	field.status = 'ready'
        	field.save()
        self.stdout.write("finished")