# Generated by Django 4.2 on 2023-06-08 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product_quantity_purchased'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rate',
            field=models.IntegerField(default=0),
        ),
    ]
