# Generated by Django 2.1.9 on 2020-01-11 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0004_auto_20200110_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='team_type',
            field=models.CharField(choices=[('0', 'ثبت نام شرکت کنندگان در مسابقه'), ('1', 'ثبت نام آزاد (خارج از مسابقه)')], max_length=1),
        ),
    ]
