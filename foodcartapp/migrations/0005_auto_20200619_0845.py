# Generated by Django 3.0.7 on 2020-06-19 08:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("foodcartapp", "0004_auto_20200619_0843"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="OrderDetails",
            new_name="OrderPosition",
        ),
    ]
