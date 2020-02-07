from django.db import models

from django.contrib.auth.models import User



def student_card_image_upload_location(instance, filename):
    return "dorm_user/%s/student-card.%s" % (instance.national_id, filename.split('.')[-1])


def national_card_image_upload_location(instance, filename):
    return "dorm_user/%s/national-card.%s" % (instance.national_id, filename.split('.')[-1])


class DormPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="dorm_payments")

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


class DormUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="dorm_users")

    name = models.CharField(max_length= 150)
    sex = models.BooleanField(default = 0)# 0: male, 1:female

    day1 = models.BooleanField(default=0)
    day2 = models.BooleanField(default=0)
    national_id = model.CharField(max_length=20)
    student_card_image = models.ImageField(upload_to=student_card_image_upload_location,
                                           null=True,
                                           blank=True,
                                           width_field="student_card_height_field",
                                           height_field="student_card_width_field")
    student_card_height_field = models.IntegerField(default=0, null=True)
    student_card_width_field = models.IntegerField(default=0, null=True)

    national_card_image = models.ImageField(upload_to=national_card_image_upload_location,
                                            null=True,
                                            blank=True,
                                            width_field="national_card_height_field",
                                            height_field="national_card_width_field")
    national_card_height_field = models.IntegerField(default=0, null=True)
    national_card_width_field = models.IntegerField(default=0, null=True)
