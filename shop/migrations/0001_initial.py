# Generated by Django 4.2 on 2023-06-12 13:44

import ckeditor_uploader.fields
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('image', models.ImageField(default='shop_media/default.png', upload_to='shop_media/category/')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('image', models.ImageField(default='shop_media/default.png', upload_to='shop_media/category/')),
                ('Category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('price', models.FloatField(default=0.0)),
                ('priceOrg', models.FloatField(null=True)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('public_day', models.DateField(default=datetime.date.today)),
                ('image', models.ImageField(default='shop_media/default.png', upload_to='shop_media/product/')),
                ('banner', models.ImageField(default='shop_media/default.png', upload_to='shop_media/product/')),
                ('viewed', models.IntegerField(default=0)),
                ('quantity_purchased', models.IntegerField(default=0)),
                ('rate', models.FloatField(default=0)),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.subcategory')),
            ],
        ),
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
