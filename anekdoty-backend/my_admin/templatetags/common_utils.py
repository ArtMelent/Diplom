from django import template
from django.contrib import admin
# from directory.models import Languages

# import directory.models

register = template.Library()


class CustomRequest:
    def __init__(self, user):
        self.user = user


@register.simple_tag(takes_context=True)
def get_app_list(context, **kwargs):
    custom_request = CustomRequest(context['request'].user)
    app_list = admin.site.get_app_list(custom_request)
    return app_list


def get_language_list(context, **kwargs):
    language_list = Languages.objects.all()
    context = {
        language_list: "directory"
    }
    return context
# @register.filter
# def get_language_list(lang_url, request):
#     languages_data = Languages.objects.all().get(url=lang_url)
#     lang_data = Languages.objects.all().values()
#     context = {
#         'languages': languages_data,
#         'lang': lang_data,
#     }
#     custom_request = CustomRequest(context['request'].name)
#     language_list = admin.site.get_language_list(custom_request)
#     return language_list
