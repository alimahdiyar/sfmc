# Generated by Django 2.1.9 on 2020-01-17 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0015_auto_20200117_0829'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='participant',
            field=models.ManyToManyField(blank=True, related_name='participant_teams', to='competition.Participant'),
        ),
        migrations.AlterField(
            model_name='team',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='teams', to='competition.Participant'),
        ),
    ]
