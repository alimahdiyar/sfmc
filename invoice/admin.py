from django.contrib import admin
from invoice.models import Invoice

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'success', 'start_date', 'update_date', 'ref_id']

admin.site.register(Invoice, InvoiceAdmin)
