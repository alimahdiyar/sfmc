# Generated by Django 2.1.9 on 2020-02-09 16:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import dorm.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DormPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('success', models.BooleanField(default=False)),
                ('error_code', models.IntegerField(default=0)),
                ('error_description', models.CharField(blank=True, default='درخواست شروع پرداخت برای بانک ارسال شده است.', max_length=300)),
                ('ref_id', models.CharField(blank=True, max_length=40, null=True)),
                ('res_code', models.IntegerField(blank=True, null=True)),
                ('sale_orderId', models.CharField(blank=True, max_length=40, null=True)),
                ('sale_referenceId', models.CharField(blank=True, max_length=40, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='dorm_payments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DormUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('gender', models.BooleanField(default=0)),
                ('day1', models.BooleanField(default=0)),
                ('day2', models.BooleanField(default=0)),
                ('national_id', models.CharField(max_length=20)),
                ('student_card_image', models.ImageField(blank=True, height_field='student_card_width_field', null=True, upload_to=dorm.models.student_card_image_upload_location, width_field='student_card_height_field')),
                ('student_card_height_field', models.IntegerField(default=0, null=True)),
                ('student_card_width_field', models.IntegerField(default=0, null=True)),
                ('national_card_image', models.ImageField(blank=True, height_field='national_card_width_field', null=True, upload_to=dorm.models.national_card_image_upload_location, width_field='national_card_height_field')),
                ('national_card_height_field', models.IntegerField(default=0, null=True)),
                ('national_card_width_field', models.IntegerField(default=0, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='dorm_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
