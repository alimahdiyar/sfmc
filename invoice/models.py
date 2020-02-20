from django.db import models
# Create your models here.

class Invoice(models.Model):
    owner = models.ForeignKey("competition.Participant", null=True, blank=True, on_delete=models.PROTECT, related_name="invoices")

    amount = models.IntegerField()

    update_date = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField(auto_now_add=True)

    success = models.BooleanField(default=False)
    error_code = models.IntegerField(default=0)
    error_description = models.CharField(max_length=300, blank=True,
                                         default='درخواست شروع پرداخت برای بانک ارسال شده است.')

    ref_id = models.CharField(max_length=40, null=True, blank=True)
    res_code = models.IntegerField(null=True, blank=True)
    sale_orderId = models.CharField(max_length=40, null=True, blank=True)
    sale_referenceId = models.CharField(max_length=40, null=True, blank=True)


    def __str__(self):
        return self.owner.name + " | " + str(self.amount) + " | " + ('موفق' if self.success else 'ناموفق')
    #Do whatever you want here
    #Did whatever i wanted here
