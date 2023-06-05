from django.apps import AppConfig


class CategoryDefaultConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'category_default'
    verbose_name = 'Category(default)'
