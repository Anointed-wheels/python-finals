# Generated by Django 5.2.1 on 2025-05-22 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_bookingmodel_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BookingModel',
        ),
    ]
