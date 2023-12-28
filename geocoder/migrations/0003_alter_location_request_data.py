# Generated by Django 3.2.15 on 2023-12-09 09:25

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ("geocoder", "0002_alter_location_latitude_alter_location_longitude_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="location",
            name="request_data",
            field=models.DateTimeField(
                db_index=True,
                default=datetime.datetime(2023, 12, 9, 9, 25, 48, 315458, tzinfo=utc),
                verbose_name="Дата запроса",
            ),
        ),
    ]