# Generated by Django 3.2.15 on 2023-11-25 03:36

from django.db import migrations


def calculate_price_order(apps, schema_editor):
    ProductOrder = apps.get_model("foodcartapp", "ProductOrder")
    ordered_products = ProductOrder.objects.all()

    for ordered_product in ordered_products.iterator():
        ordered_product.price = ordered_product.quantity * ordered_product.product.price
        ordered_product.save()


class Migration(migrations.Migration):
    dependencies = [
        ("foodcartapp", "0043_productorder_price"),
    ]

    operations = [
        migrations.RunPython(calculate_price_order),
    ]
