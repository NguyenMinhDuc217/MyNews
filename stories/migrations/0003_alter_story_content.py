# Generated by Django 4.2 on 2023-06-06 03:52

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0002_alter_story_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
