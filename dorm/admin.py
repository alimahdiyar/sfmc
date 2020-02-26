from django.contrib import admin
from .models import DormUser,DormPayment
# Register your models here.

class DormUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'day1', 'day2']

class DormPaymentAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'success', 'start_date', 'update_date', 'ref_id']

admin.site.register(DormUser, DormUserAdmin)
admin.site.register(DormPayment, DormPaymentAdmin)
