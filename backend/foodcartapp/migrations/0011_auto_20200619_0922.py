# Generated by Django 3.0.7 on 2020-06-19 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("foodcartapp", "0010_auto_20200619_0921"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hotel",
            name="city",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="hotels",
                to="foodcartapp.City",
                verbose_name="город",
            ),
        ),
    ]
