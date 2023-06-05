

from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader


from directory.models import Languages
from category_default.models import Tags


# Create your views here.

def language_filter(request):
    languages_data = Languages.objects.all()
    context = {
        'languages': languages_data,
    }
    template = loader.get_template('test.html')
    return HttpResponse(template.render(context, request))


def category_default_app(request, lang_slug):
    language_data = Languages.objects.get(url=lang_slug)
    context = {
        language_data: 'languages'
    }
    return render(request, 'category_default_app.html', context)


def tags_create(request, tag_slug, lang_slug):
    language_data = Languages.objects.get(url=lang_slug)
    tags_data = Languages.objects.get(url=tag_slug)


def base_html(request):
    language_data = Languages.objects.all()
    context = {
        language_data: 'lang'
    }
    return render(request, 'admin/base.html', context)


