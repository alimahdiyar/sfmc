# Generated by Django 2.1.9 on 2020-01-10 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0003_auto_20200108_0453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='team_type',
            field=models.CharField(choices=[('0', 'ثبت نام آزاد (خارج از مسابقه)'), ('1', 'ثبت نام شرکت کنندگان در مسابقه')], max_length=1),
        ),
    ]