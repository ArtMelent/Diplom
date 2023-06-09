# Generated by Django 4.1.2 on 2022-12-18 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('directory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('seo_title', models.CharField(max_length=255)),
                ('seo_description', models.TextField(blank=True, null=True)),
                ('seo_h1', models.CharField(blank=True, max_length=255, null=True)),
                ('seo_keywords', models.CharField(blank=True, max_length=255, null=True)),
                ('breadcrumb', models.CharField(blank=True, max_length=255, null=True)),
                ('url', models.CharField(blank=True, max_length=255, null=True)),
                ('image_url', models.ImageField(upload_to='tags', verbose_name='Image')),
                ('visible', models.BooleanField(default=True)),
                ('alternative', models.BooleanField(default=False)),
                ('records_per_page', models.IntegerField(default=20, verbose_name=range(5, 50))),
                ('parsing_words', models.CharField(blank=True, max_length=255, null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('anchor1', models.CharField(blank=True, max_length=255, null=True)),
                ('anchor2', models.CharField(blank=True, max_length=255, null=True)),
                ('anchor3', models.CharField(blank=True, max_length=255, null=True)),
                ('anchor4', models.CharField(blank=True, max_length=255, null=True)),
                ('anchor5', models.CharField(blank=True, max_length=255, null=True)),
                ('anchor6', models.CharField(blank=True, max_length=255, null=True)),
                ('anchor7', models.CharField(blank=True, max_length=255, null=True)),
                ('anchor8', models.CharField(blank=True, max_length=255, null=True)),
                ('anchor9', models.CharField(blank=True, max_length=255, null=True)),
                ('anchor10', models.CharField(blank=True, max_length=255, null=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='directory.languages')),
                ('tag_down', models.ManyToManyField(blank=True, to='category_default.tags')),
                ('tag_mid', models.ManyToManyField(blank='True', to='category_default.tags')),
            ],
            options={
                'verbose_name_plural': 'Tags',
                'db_table': 'tags',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, null=True)),
                ('url', models.CharField(max_length=45)),
                ('description', models.TextField()),
                ('image_url', models.ImageField(upload_to='category', verbose_name='Image')),
                ('seo_title', models.CharField(max_length=45)),
                ('seo_description', models.TextField(blank=True, null=True)),
                ('seo_h1', models.CharField(blank=True, max_length=45, null=True)),
                ('visible', models.BooleanField(default=False)),
                ('shown_in_menu', models.BooleanField(default=False)),
                ('alternative', models.BooleanField(default=False)),
                ('behave_as_tag', models.BooleanField(default=False)),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('date_modified', models.DateField(auto_now_add=True, null=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='directory.languages')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='category_default.categories')),
                ('tags', models.ManyToManyField(to='category_default.tags')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'db_table': 'categories',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Anekdots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('h2', models.CharField(blank=True, max_length=255)),
                ('text', models.TextField(blank=True, null=True)),
                ('rating', models.IntegerField(blank=True, default=0, null=True)),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('date_modified', models.DateField(auto_now_add=True, null=True)),
                ('category', models.ManyToManyField(blank='True', to='category_default.categories')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='directory.languages')),
                ('tags', models.ManyToManyField(to='category_default.tags')),
            ],
            options={
                'verbose_name_plural': 'Anekdots',
                'db_table': 'anekdots',
                'managed': True,
            },
        ),
    ]
