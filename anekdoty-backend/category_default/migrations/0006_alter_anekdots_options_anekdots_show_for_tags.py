# Generated by Django 4.1.2 on 2023-01-02 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category_default', '0005_remove_categories_parent_categories_parent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='anekdots',
            options={'managed': True, 'verbose_name_plural': 'Records'},
        ),
        migrations.AddField(
            model_name='anekdots',
            name='show_for_tags',
            field=models.ManyToManyField(related_name='+', to='category_default.tags'),
        ),
    ]
