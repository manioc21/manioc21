from django.db import models
from django.contrib.postgres.fields import JSONField
from authenticate.models import User

# Create your models here.

FIELD_STATUS = (
    ('ready','Ready'),
    ('not_ready','Not ready'),
    ('harvest','Harvest')
)

FARMER_STATUS = (
    ('active','Active'),
    ('inactive','Inactive'),
    ('dead','Dead')
)

class Coop(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Farmer(models.Model):
    coop = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    data = JSONField(null=True,blank=True)
    status = models.CharField(max_length=50,default='active',choices=FARMER_STATUS)

class Field(models.Model):
    coop = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    data = JSONField()
    status = models.CharField(max_length=50,default='not_ready',choices=FIELD_STATUS)

class Payment(models.Model):
    farmer = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now=True)

class Stock(models.Model):
    coop = models.ForeignKey(User, on_delete=models.CASCADE)
    data = JSONField()

class Sales(models.Model):
    coop = models.ForeignKey(User, on_delete=models.CASCADE)
    data = JSONField()

class Supply(models.Model):
    coop = models.ForeignKey(User, on_delete=models.CASCADE)
    data = JSONField()

class TransformedProduct(models.Model):
    coop = models.ForeignKey(User, on_delete=models.CASCADE)
    data = JSONField()

class Pest(models.Model):
    coop = models.ForeignKey(User, on_delete=models.CASCADE)
    data = JSONField()

class Message(models.Model):
    body = models.TextField()
    phone = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.body
