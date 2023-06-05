from django.db import models
from django.urls import reverse

from django.shortcuts import get_object_or_404


# Create your models here.
class Languages(models.Model):
    code = models.CharField(unique=True, max_length=5,)
    name = models.CharField(max_length=30,)
    url = models.CharField(max_length=30, blank=True)

    class Meta:
        managed = True
        db_table = 'languages'
        verbose_name_plural = 'Languages'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_default:language_set', kwargs={'lang_url': self.url})

    def url_name(self):
        return self.url

    def set_current_language(modeladmin, request, queryset):
        org = queryset.first()
        if org:
            request.session["admin_current_language"] = {
                "id": str(org.id),
                "name": org.name,
            }

    set_current_language.short_description = "Set language as current language"

    def clear_current_language(modeladmin, request, queryset):
        del request.session["admin_current_language"]

    clear_current_language.short_description = "Clear current language choice"