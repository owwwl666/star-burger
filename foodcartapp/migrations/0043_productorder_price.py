# Generated by Django 3.2.15 on 2023-11-25 03:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0042_auto_20231125_0209'),
    ]

    operations = [
        migrations.AddField(
            model_name='productorder',
            name='price',
            field=models.DecimalField(db_index=True, decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена заказа'),
        ),
    ]
