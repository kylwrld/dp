# Generated by Django 4.2.4 on 2023-11-19 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_profile_lastname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='lastname',
        ),
    ]
