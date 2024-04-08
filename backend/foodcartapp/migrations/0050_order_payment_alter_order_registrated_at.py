# Generated by Django 4.2.7 on 2023-11-28 12:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("foodcartapp", "0049_order_called_at_order_delivered_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="payment",
            field=models.CharField(
                blank=True,
                choices=[("cash", "Наличностью"), ("non-cash", "Электронно")],
                db_index=True,
                default="cash",
                max_length=30,
                null=True,
                verbose_name="Способ оплаты",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="registrated_at",
            field=models.DateTimeField(
                db_index=True,
                default=datetime.datetime(
                    2023, 11, 28, 12, 9, 28, 799273, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Дата создания заказа",
            ),
        ),
    ]