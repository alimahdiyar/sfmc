from django.contrib import admin
from .models import DormUser,DormPayment
# Register your models here.

admin.site.register(DormUser)
admin.site.register(DormPayment)
