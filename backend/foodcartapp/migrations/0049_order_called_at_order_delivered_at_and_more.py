# Generated by Django 4.2.7 on 2023-11-28 11:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("foodcartapp", "0048_order_registrated_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="called_at",
            field=models.DateTimeField(
                blank=True,
                db_index=True,
                null=True,
                verbose_name="Дата звонка менеджера",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="delivered_at",
            field=models.DateTimeField(
                blank=True, db_index=True, null=True, verbose_name="Дата доставки"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="registrated_at",
            field=models.DateTimeField(
                db_index=True,
                default=datetime.datetime(
                    2023, 11, 28, 11, 56, 6, 637417, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Дата создания заказа",
            ),
        ),
    ]
