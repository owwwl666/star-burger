# Generated by Django 3.2.15 on 2023-12-11 10:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ("geocoder", "0007_alter_location_request_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="location",
            name="request_data",
            field=models.DateTimeField(
                db_index=True,
                default=datetime.datetime(2023, 12, 11, 10, 10, 40, 740358, tzinfo=utc),
                verbose_name="Дата запроса",
            ),
        ),
    ]
