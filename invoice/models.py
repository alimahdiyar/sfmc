from django.db import models

# Create your models here.

class Invoice(models.Model):
    amount = models.IntegerField()

    #Do whatever you want here