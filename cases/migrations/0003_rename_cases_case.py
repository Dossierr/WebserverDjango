# Generated by Django 4.1.7 on 2023-12-24 05:31

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cases', '0002_rename_yourmodel_cases'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cases',
            new_name='Case',
        ),
    ]
