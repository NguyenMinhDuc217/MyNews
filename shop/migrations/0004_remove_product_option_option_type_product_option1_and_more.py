# Generated by Django 4.2 on 2023-06-23 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_product_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='option',
        ),
        migrations.AddField(
            model_name='option',
            name='type',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='product',
            name='option1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='option2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='option3',
            field=models.IntegerField(default=0),
        ),
    ]
