# Generated by Django 4.2 on 2023-06-29 08:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_remove_product_option_option_type_product_option1_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('namecode', models.CharField(max_length=150)),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=150)),
                ('value', models.CharField(max_length=150)),
                ('type', models.CharField(max_length=150)),
                ('day_start', models.DateTimeField(default=django.utils.timezone.now)),
                ('day_end', models.DateTimeField(default=django.utils.timezone.now)),
                ('pay_method', models.CharField(max_length=150)),
                ('status', models.IntegerField(choices=[(0, 'failed'), (1, 'success'), (2, 'wait')])),
            ],
        ),
    ]