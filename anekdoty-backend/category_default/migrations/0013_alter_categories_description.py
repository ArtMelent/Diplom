# Generated by Django 4.1.2 on 2023-05-17 02:00

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category_default', '0012_tags_only_subtag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]