from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Coop)
admin.site.register(Farmer)
admin.site.register(Field)
admin.site.register(Payment)
admin.site.register(Sales)
admin.site.register(Stock)
admin.site.register(Supply)
admin.site.register(TransformedProduct)
admin.site.register(Message)