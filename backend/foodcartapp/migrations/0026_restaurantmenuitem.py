# Generated by Django 3.0.7 on 2020-06-29 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("foodcartapp", "0025_auto_20200629_1004"),
    ]

    operations = [
        migrations.CreateModel(
            name="RestaurantMenuItem",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "availability",
                    models.BooleanField(
                        db_index=True, default=True, verbose_name="в продаже"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="menu_items",
                        to="foodcartapp.Product",
                    ),
                ),
                (
                    "restaurant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="menu_items",
                        to="foodcartapp.Restaurant",
                    ),
                ),
            ],
            options={
                "verbose_name": "пункт меню ресторана",
                "verbose_name_plural": "пункты меню ресторана",
            },
        ),
    ]
