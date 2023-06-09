# Generated by Django 4.2 on 2023-06-09 04:11

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_product_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('quantility', models.IntegerField(default=0)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField()),
                ('status', models.IntegerField(choices=[(0, 'failed'), (1, 'success'), (2, 'wait')])),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.product')),
            ],
        ),
    ]