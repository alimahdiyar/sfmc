# Generated by Django 2.1.9 on 2020-01-11 10:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0009_remove_competitionfield_can_free_register'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advisor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('university', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='uploadedfile',
            name='team',
        ),
        migrations.AddField(
            model_name='participant',
            name='national_card_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='participant',
            name='organization',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='team',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='members', to='competition.Team'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='upload_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='uploaded_file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='participant',
            name='student_card_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='participant',
            name='university',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='participant',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='team', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='UploadedFile',
        ),
        migrations.AddField(
            model_name='team',
            name='advisor',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='team', to='competition.Advisor'),
        ),
    ]