from django.core.management.base import BaseCommand
from mainapp.models import Field
import datetime

class Command(BaseCommand):
    help = 'Check harvest'

    def handle(self, *args, **kwargs):
        today = datetime.date.today()
        fields = Field.objects.filter(data__harvestdate__lte=str(today),status='not_ready')
        for field in fields:
        	field.status = 'ready'
        	field.save()
        max_date = today - datetime.timedelta(days=60)
        fields = Field.objects.filter(data__harvestdate=str(max_date))
        for field in fields:
        	field.status = 'harvest'
        	field.history = True
        	field.save()
        self.stdout.write("finished")