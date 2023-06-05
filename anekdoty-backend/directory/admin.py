import uuid

from django.contrib import admin
from django.utils.html import format_html

from .models import *
from django.contrib.admin.filters import AllValuesFieldListFilter
from category_default.models import *


# from tags.models import *
# from category_default.admin import anekdoty_site

class DropdownFilter(AllValuesFieldListFilter):
    template = 'admin/dropdown_filter.html'


class InlineEditLinkMixin(object):
    readonly_fields = ['edit_details']
    edit_label = "Edit"

    def edit_details(self, obj):
        if obj.id:
            opts = self.model._meta
            return "<a href='%s' target='_blank'>%s</a>" % (reverse(
                'admin:%s_%s_change' % (opts.app_label, opts.object_name.lower()),
                args=[obj.id]
            ), self.edit_label)
        else:
            return "(save to edit details)"

    edit_details.allow_tags = True


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'description', 'seo_title', 'seo_description', 'seo_h1', 'breadcrumb', 'url',
        'visible',
        'alternative', 'records_per_page', 'parsing_words')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    list_editable = ('visible', 'alternative')
    list_filter = (('language__name', DropdownFilter),)
    fieldsets = [
        ('Content', {'fields': ['language', 'name', 'description', 'image_url', 'url'],
                     # 'classes': ('collapse', 'wide'),
                     }),
        ('Seo settings', {
            'fields': ['seo_title', 'seo_description', 'seo_h1', 'seo_keywords', 'breadcrumb',
                       'parsing_words', ('visible', 'alternative'), 'records_per_page', 'tag_mid', 'tag_down'],
            'classes': ('collapse', 'extrapretty'),
        }),
        ('Anchor words', {
            'fields': [('anchor1', 'anchor2'), ('anchor3', 'anchor4'), ('anchor5', 'anchor6'), ('anchor7', 'anchor8'),
                       ('anchor9', 'anchor10')],
            'classes': ('collapse',),
        })
    ]
    autocomplete_fields = ['tag_mid', 'tag_down']


class TagInline(InlineEditLinkMixin, admin.StackedInline):
    model = Tags
    fieldsets = [
        ('Content', {'fields': ['language', 'name', 'description', 'image_url', 'url', ],
                     'classes': ('collapse', 'wide'),
                     }),
        ('Seo settings', {
            'fields': ['seo_title', 'seo_description', 'seo_h1', 'seo_keywords', 'breadcrumb',
                       'parsing_words', ('visible', 'alternative'), 'records_per_page', 'tag_mid', 'tag_down'],
            'classes': ('collapse',),
        }),
        ('Anchor words', {
            'fields': [('anchor1', 'anchor2'), ('anchor3', 'anchor4'), ('anchor5', 'anchor6'), ('anchor7', 'anchor8'),
                       ('anchor9', 'anchor10')],
            'classes': ('collapse',),
        })
    ]
    #
    classes = ['collapse']
    autocomplete_fields = ['tag_mid', 'tag_down']
    # search_field = ["name", ]
    extra = 0
    show_change_link = True


class CategoryInline(admin.StackedInline):
    model = Categories
    classes = ['collapse']
    extra = 0


@admin.action(description='Set current language')
def set_current_organisation(modeladmin, request, queryset):
    org = queryset.first()
    if org:
        request.session["admin_current_organization"] = {
            "id": str(org.id),
            "name": org.name,
        }


@admin.action(description='Clear current language choice')
def clear_current_organisation(modeladmin, request, queryset):
    del request.session["admin_current_organization"]


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'url')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    fieldsets = [
        ('Languages', {
            'fields': ['name', 'code', 'url'],
            # 'classes': ('collapse',),
        })
    ]
    list_filter = (
        ('name', DropdownFilter),
    )
    # inlines = [CategoryInline, TagInline]
    # classes = ['collapse']
    show_in_index = True
    actions = [set_current_organisation, clear_current_organisation]


# Register your models here.
admin.site.register(Languages, LanguageAdmin)
