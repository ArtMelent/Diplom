from django.contrib import admin
from django.contrib.admin import AllValuesFieldListFilter

from .models import *
from directory.models import *


class DropdownFilter(AllValuesFieldListFilter):
    template = 'admin/dropdown_filter.html'


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'description', 'seo_title', 'seo_description', 'seo_h1', 'breadcrumb', 'url',
        'records_per_page', 'parsing_words')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    # list_filter = (('language__name', DropdownFilter),)
    list_filter = ('language',)
    fieldsets = [
        (None, {
            'fields': ['language'],
            'classes': ('collapse',),
        }),
        ('Content', {'fields': ['name', 'description', 'image_url', 'url', 'sub_tags', 'only_subtag'],
                     # 'classes': ('collapse', 'wide'),
                     }),
        ('Seo settings', {
            'fields': ['seo_title', 'seo_description', 'seo_h1', 'seo_keywords', 'breadcrumb',
                       'parsing_words', 'records_per_page', 
                    #    'tag_mid', 'tag_down'
                       ],
            'classes': ('collapse', 'extrapretty'),
        }),
        # ('Anchor words', {
        #     'fields': [('anchor1', 'anchor2'), ('anchor3', 'anchor4'), ('anchor5', 'anchor6'), ('anchor7', 'anchor8'),
        #                ('anchor9', 'anchor10')],
        #     'classes': ('collapse',),
        # })
    ]
    # readonly_fields = ['language']
    # autocomplete_fields = ['tag_mid', 'tag_down', ]
    autocomplete_fields = ['sub_tags', ]

    # prepopulated_fields = {'name': ('fk_name',)}
    def get_list_filter(self, request):
        """
        If an current organization is set we exclude the list filter for organizations
        """
        current_admin_org = request.session.get("admin_current_organization")
        if current_admin_org is not None:
            new_list_filter = []
            for old_filter in super().get_list_filter(request):
                if not old_filter.startswith("language"):
                    new_list_filter.append(old_filter)
            return tuple(new_list_filter)
        else:
            return super().get_list_filter(request)

    def get_changeform_initial_data(self, request):
        """
        If a current organization is set we set it as default on new objects.
        """
        current_admin_org = request.session.get("admin_current_organization")
        initial_data = super().get_changeform_initial_data(request)
        if current_admin_org is not None:
            initial_data["language"] = current_admin_org["id"]

        return initial_data

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Exclude objects not belonging to model in many to many
        """
        db = kwargs.get("using")
        if "queryset" not in kwargs:
            queryset = self.get_field_queryset(db, db_field, request)
            if queryset is not None:
                kwargs["queryset"] = queryset

        current_admin_org = request.session.get("admin_current_organization")

        if current_admin_org:
            qs = kwargs.get("queryset")
            if qs:
                qs = qs.filter(language__id=current_admin_org["id"])
                kwargs["queryset"] = qs
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_search_results(self, request, queryset, search_term):
        """
        Will filter the whole list result set to the current active organization.
        it will also filter autocomplete fields.
        """
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        current_admin_org = request.session.get("admin_current_organization")

        if current_admin_org:
            queryset = queryset.filter(
                language__id=current_admin_org["id"]
            )

        return queryset, use_distinct


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # 'anekdot_id',
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    autocomplete_fields = ['tags', 'sub_categories', 'language']
    list_filter = ('language',)
    fieldsets = [
        (None, {
            'fields': ['language'],
            'classes': ('collapse',),
        }),
        ('Category', {
            'fields': ['sub_categories', 'tags', 'name', 'url', 'description', 'image_url', 'seo_title', 'seo_description',
                       'seo_h1', ('shown_in_menu', 'behave_as_tag')],
        })
    ]

    def get_list_filter(self, request):
        """
        If an current organization is set we exclude the list filter for organizations
        """
        current_admin_org = request.session.get("admin_current_organization")
        if current_admin_org is not None:
            new_list_filter = []
            for old_filter in super().get_list_filter(request):
                if not old_filter.startswith("language"):
                    new_list_filter.append(old_filter)
            return tuple(new_list_filter)
        else:
            return super().get_list_filter(request)

    def get_changeform_initial_data(self, request):
        """
        If a current organization is set we set it as default on new objects.
        """
        current_admin_org = request.session.get("admin_current_organization")
        initial_data = super().get_changeform_initial_data(request)
        if current_admin_org is not None:
            initial_data["language"] = current_admin_org["id"]

        return initial_data

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Exclude objects not belonging to model in many to many
        """
        db = kwargs.get("using")
        if "queryset" not in kwargs:
            queryset = self.get_field_queryset(db, db_field, request)
            if queryset is not None:
                kwargs["queryset"] = queryset

        current_admin_org = request.session.get("admin_current_organization")

        if current_admin_org:
            qs = kwargs.get("queryset")
            if qs:
                qs = qs.filter(language__id=current_admin_org["id"])
                kwargs["queryset"] = qs
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_search_results(self, request, queryset, search_term):
        """
        Will filter the whole list result set to the current active organization.
        it will also filter autocomplete fields.
        """
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        current_admin_org = request.session.get("admin_current_organization")

        if current_admin_org:
            queryset = queryset.filter(
                language__id=current_admin_org["id"]
            )

        return queryset, use_distinct


class AnecdoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'h2', 'text', 'rating')
    list_display_links = ('id', 'h2')
    search_fields = ('id', 'h2')
    autocomplete_fields = ['category', 'tags']
    fieldsets = [
        (None, {
            'fields': ['language'],
            'classes': ('collapse',),
        }),
        (None, {
            'fields': ['tags', 'category', 'text', ('rating', 'h2')],
        })
    ]
    list_filter = ['language']

    def get_list_filter(self, request):
        """
        If an current organization is set we exclude the list filter for organizations
        """
        current_admin_org = request.session.get("admin_current_organization")
        if current_admin_org is not None:
            new_list_filter = []
            for old_filter in super().get_list_filter(request):
                if not old_filter.startswith("language"):
                    new_list_filter.append(old_filter)
            return tuple(new_list_filter)
        else:
            return super().get_list_filter(request)

    def get_changeform_initial_data(self, request):
        """
        If a current organization is set we set it as default on new objects.
        """
        current_admin_org = request.session.get("admin_current_organization")
        initial_data = super().get_changeform_initial_data(request)
        if current_admin_org is not None:
            initial_data["language"] = current_admin_org["id"]

        return initial_data

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Exclude objects not belonging to model in many to many
        """
        db = kwargs.get("using")
        if "queryset" not in kwargs:
            queryset = self.get_field_queryset(db, db_field, request)
            if queryset is not None:
                kwargs["queryset"] = queryset

        current_admin_org = request.session.get("admin_current_organization")

        if current_admin_org:
            qs = kwargs.get("queryset")
            if qs:
                qs = qs.filter(language__id=current_admin_org["id"])
                kwargs["queryset"] = qs
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_search_results(self, request, queryset, search_term):
        """
        Will filter the whole list result set to the current active organization.
        it will also filter autocomplete fields.
        """
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        current_admin_org = request.session.get("admin_current_organization")

        if current_admin_org:
            queryset = queryset.filter(
                language__id=current_admin_org["id"]
            )

        return queryset, use_distinct

admin.site.site_header = 'Anecdote admin'

admin.site.register(Anekdots, AnecdoteAdmin)
admin.site.register(Tags, TagAdmin)
admin.site.register(Categories, CategoryAdmin)
