# Generated by Django 4.1.2 on 2022-12-19 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category_default', '0002_alter_tags_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='tag_mid',
            field=models.ManyToManyField(blank=True, to='category_default.tags'),
        ),
    ]