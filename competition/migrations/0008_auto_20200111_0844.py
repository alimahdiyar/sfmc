# Generated by Django 2.1.9 on 2020-01-11 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0007_competitionfield_needs_supervisor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='competitionfield',
            old_name='needs_supervisor',
            new_name='needs_advisor',
        ),
    ]
