# Generated by Django 2.1.9 on 2020-01-17 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0013_auto_20200117_0658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='participant_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='members', to='competition.Team'),
        ),
    ]
