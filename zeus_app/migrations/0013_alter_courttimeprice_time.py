# Generated by Django 5.2 on 2025-05-26 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zeus_app', '0012_rename_bookind_datetime_booking_booking_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courttimeprice',
            name='time',
            field=models.CharField(choices=[('06:00', '06:00'), ('08:00', '08:00'), ('10:00', '10:00'), ('12:00', '12:00'), ('14:00', '14:00'), ('16:00', '16:00'), ('18:00', '18:00'), ('20:00', '20:00'), ('22:00', '22:00')], default='00:00'),
        ),
    ]
