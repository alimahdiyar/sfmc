from django.db import models

# Create your models here.

class Invoice(models.Model):
    team = models.OneToOneField('competition.Team', null=True, blank=True, on_delete=models.PROTECT, related_name="invoice")
    amount = models.IntegerField()

    #Do whatever you want here