# Generated by Django 3.2.15 on 2023-12-09 09:41

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0055_auto_20231209_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='registered_at',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 12, 9, 9, 41, 14, 934145, tzinfo=utc), verbose_name='Дата создания заказа'),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='order_price',
            field=models.DecimalField(db_index=True, decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена заказа'),
        ),
    ]
