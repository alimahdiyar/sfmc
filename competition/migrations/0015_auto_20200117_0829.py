# Generated by Django 2.1.9 on 2020-01-17 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0014_auto_20200117_0720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='competition_field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='competition.CompetitionField'),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
