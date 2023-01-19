from django.db import models

class vendingMachine(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

class stock(models.Model):
    vm = models.ForeignKey(vendingMachine, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

