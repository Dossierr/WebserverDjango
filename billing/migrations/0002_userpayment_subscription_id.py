# Generated by Django 4.1.7 on 2023-12-26 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpayment',
            name='subscription_id',
            field=models.CharField(default='no subscription id', max_length=500),
            preserve_default=False,
        ),
    ]
