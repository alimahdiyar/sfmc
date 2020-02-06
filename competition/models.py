from django.db import models
from django.contrib.auth.models import User



# Create your models here.
from django.db.models.signals import post_save

from invoice.models import Invoice


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.PROTECT, related_name="profile")
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    national_id = models.CharField(max_length=100)
    university = models.CharField(max_length=255)

    def __str__(self):
        return self.name + " " + self.phone_number
