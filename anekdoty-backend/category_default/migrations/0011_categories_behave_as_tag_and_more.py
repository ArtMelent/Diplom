# Generated by Django 4.1.2 on 2023-05-16 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category_default', '0010_rename_parent_tag_tags_sub_tags_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='behave_as_tag',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='categories',
            name='sub_categories',
            field=models.ManyToManyField(blank=True, to='category_default.categories'),
        ),
    ]
