# Generated by Django 2.1.9 on 2020-01-02 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='manager',
            old_name='studnt_card_image',
            new_name='student_card_image',
        ),
        migrations.RenameField(
            model_name='participant',
            old_name='studnt_card_image',
            new_name='student_card_image',
        ),
    ]
