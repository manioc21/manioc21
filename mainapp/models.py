from django.db import models
from django.contrib.postgres.fields import JSONField
from authenticate.models import User

# Create your models here.

FIELD_STATUS = (
    ('ready','Mature'),
    ('not_ready','Non mature'),
    ('harvest','Deja recolte')
)

FARMER_STATUS = (
    ('active','Actif'),
    ('inactive','Inactif'),
    ('dead','Mort')
)

class Coop(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Farmer(models.Model):
    coop = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    data = JSONField(null=True,blank=True)
    status = models.CharField(max_length=50,default='active',choices=FARMER_STATUS)
    history = models.BooleanField(default=False)

class Field(models.Model):
    coop = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    data = JSONField()
    status = models.CharField(max_length=50,default='not_ready',choices=FIELD_STATUS)
    history = models.BooleanField(default=False)

class Payment(models.Model):
    farmer = models.ForeignKey(Farmer,on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now=True)
    history = models.BooleanField(default=False)

class Stock(models.Model):
    coop = models.ForeignKey(User, on_delete=models.CASCADE)
    data = JSONField()
    history = models.BooleanField(default=False)

class Sales(models.Model):
    coop = models.ForeignKey(User, on_delete=models.CASCADE)
    data = JSONField()
    history = models.BooleanField(default=False)

class Supply(models.Model):
    coop = models.ForeignKey(User, on_delete=models.CASCADE)
    data = JSONField()
    history = models.BooleanField(default=False)

class TransformedProduct(models.Model):
    coop = models.ForeignKey(User, on_delete=models.CASCADE)
    data = JSONField()
    history = models.BooleanField(default=False)

class Pest(models.Model):
    coop = models.ForeignKey(User, on_delete=models.CASCADE)
    data = JSONField()
    history = models.BooleanField(default=False)

class Message(models.Model):
    body = models.TextField()
    phone = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.body


class Chat(models.Model):
    phone = models.CharField(max_length=50)
    page = models.IntegerField()
    field = models.IntegerField(null=True)
