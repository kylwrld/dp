# Generated by Django 4.2.6 on 2023-11-22 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_profile_lastname'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='date',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='date'),
        ),
    ]