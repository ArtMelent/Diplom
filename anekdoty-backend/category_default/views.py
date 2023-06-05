from django.shortcuts import render

from rest_framework import generics
from .serializers import *

from django.utils.translation import gettext as _
from django.template.loader import render_to_string
from django.template import loader
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from .models import *
from directory.models import *
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from my_admin.templatetags.auto_link import *
from django.urls import LocalePrefixPattern, URLResolver, get_resolver, path, reverse
# from django.core.management import setup_environ
from anekdoty_app import settings
from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from django.views import View


class LanguageDataAPIView(APIView):
   def get(self, request, langUrl):
        try:
            # Retrieve language data
            language = Languages.objects.get(url=langUrl)
            language_serializer = LanguageSerializer(language)

            # Retrieve anekdoty data
            anekdoty = Anekdots.objects.filter(language=language)
            anekdoty_serializer = AnekdotySerializer(anekdoty, many=True)

            # Retrieve categories data
            categories = Categories.objects.filter(language=language)
            categories_serializer = CategorySerializer(categories, many=True)

            # Retrieve tags data
            tags = Tags.objects.filter(language=language)
            tags_serializer = TagSerializer(tags, many=True)

            # Return combined data
            data = {
                'language': language_serializer.data,
                'anekdoty': anekdoty_serializer.data,
                'categories': categories_serializer.data,
                'tags': tags_serializer.data
            }
            return JsonResponse(data)   
        except Languages.DoesNotExist:
            raise Http404("Language not found")

class CategorySharedDataAPIView(APIView):
    def get(self, request):
        language_url = request.GET.get('langUrl')

        categories = Categories.objects.filter(language=language_url).prefetch_related('sub_categories')
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data)



class CategoryDataAPIView(APIView):
    def get(self, request, language_url, category_url, subcategory_url=None):
        try:
            # Get the language and category based on the language URL and category URL
            language = Languages.objects.get(url=language_url)
            category = Categories.objects.get(url=category_url, language=language)
            
            # Check if the category is a direct child of the specified language
            subcategory = None

            if subcategory_url:
                # If a subcategory URL is present, get the subcategory and its tags
                subcategory = category.sub_categories.filter(url=subcategory_url).first()
                if subcategory:
                    # Get the common tags for the category and subcategory
                    tags_category = category.tags.all()
                    tags_subcategory = subcategory.tags.all()
                    common_tags = tags_category.filter(id__in=tags_subcategory)

                    # Get all the records for the common tags, category, and subcategory
                    records = Anekdots.objects.filter(
                        tags__in=common_tags,
                        tags__categories=category,
                        tags__categories__sub_categories=subcategory
                    ).distinct()
                else:
                    common_tags = None
                    records = None
            else:
                # If no subcategory URL is present, get the category's tags
                common_tags = category.tags.all()
                records = Anekdots.objects.filter(tags__in=common_tags, tags__categories=category).distinct()

            if subcategory_url and not subcategory:
                raise Http404(f"Subcategory '{subcategory_url}' not found in category '{category_url}'")

            # Serialize the data
            language_serializer = LanguageSerializer(language)
            category_serializer = CategorySerializer(category)
            subcategory_serializer = SubCategorySerializer(subcategory) if subcategory else None  # Use SubCategorySerializer
            anekdots_serializer = AnekdotySerializer(records, many=True)
            tags_serializer = TagSerializer(common_tags, many=True)

            # Return the combined data
            data = {
                'language': language_serializer.data,
                'category': category_serializer.data,
                'subcategory': subcategory_serializer.data if subcategory else None,
                'common_tags': tags_serializer.data,
                'records': anekdots_serializer.data,
                'subcategory_url': subcategory.url if subcategory else None
            }

            return Response(data)

        except Languages.DoesNotExist:
            raise Http404("Language not found")

        except Categories.DoesNotExist:
            raise Http404("Category not found")


class NotFoundAPIView(View):
    def get(self, request, path):
        # Redirect to the previous page
        previous_url = request.META.get('HTTP_REFERER')
        if previous_url:
            return HttpResponseRedirect(previous_url)
        else:
            # If there is no previous page, redirect to a default page
            return HttpResponseRedirect('/')   

class TagsAPIView(APIView):
    def get(self, request, language_url, category_url, subcategory_url=None, tag_url=None, subtag_url=None):
        # Get the language, category, and subcategory based on the language URL, category URL, and subcategory URL
        language = get_object_or_404(Languages, url=language_url)
        category = get_object_or_404(Categories, url=category_url, language=language)
        subcategory = None
        if subcategory_url:
            subcategory = category.sub_categories.filter(url=subcategory_url).first()

        # Get the tag and subtag based on the tag URL and subtag URL
        tag = None
        subtag = None
        if tag_url:
            tag = get_object_or_404(Tags, url=tag_url, categories=category)
            if subtag_url:
                # check if subtag exists and it is common with the category and tag
                subtag = tag.sub_tags.filter(url=subtag_url, categories=category).first()
                if not subtag:
                    raise Http404("Subtag not found")

        # Get the records based on the tag, subtag, category, and subcategory (if present)
        records = None
        if tag:
            records = Anekdots.objects.filter(tags=tag)
            if subtag:
                records = records.filter(tags=subtag)
        elif category:
            common_tags = category.tags.all()
            if subcategory:
                # check if subcategory is common with the category and tag (if present)
                sub_tags = subcategory.tags.all()
                if tag:
                    sub_tags = sub_tags.filter(categories=category, sub_tags__in=[tag])
                    common_tags = common_tags.intersection(sub_tags)
                    records = Anekdots.objects.filter(tags__in=common_tags, tags__categories=category)
            if subcategory:
                records = records.filter(tags__categories__sub_categories=subcategory)

        # Serialize the data
        tags_serializer = TagSerializer(tag)
        anekdots_serializer = AnekdotySerializer(records, many=True)
        language_serializer = LanguageSerializer(language)
        category_serializer = CategorySerializer(category)
        subcategory_serializer = SubCategorySerializer(subcategory)
        subtag_serializer = TagSerializer(subtag)  # Add this line

        # Construct the response data
        data = {
            'language': language_serializer.data,
            'category': category_serializer.data,
            'subcategory': subcategory_serializer.data,
            'tag': tags_serializer.data,
            'subtag': subtag_serializer.data,  # Update this line
            'records': anekdots_serializer.data,
            'current_tag': tags_serializer.data,
        }

        return Response(data)


def language_set(request, url):
    languages_data = Languages.objects.all().get(url=url)
    categories_data = Categories.objects.filter(language=languages_data)
    tags_data = Tags.objects.all().filter(language=languages_data)
    records_data = Anekdots.objects.filter(tags__language=languages_data)
    lang_data = Languages.objects.all().values()


    context = {
        'languages': languages_data,
        'tags': tags_data,
        'categories': categories_data,
        'records': records_data,
    }

    # return JsonResponse(data)
    template = loader.get_template('home_page.html')
    return HttpResponse(template.render(context, request))

from django.db.models import Subquery, OuterRef



def category(request, language_url, category_url, subcategory_url=None):
    # Get the language and category based on the language URL and category name
    language = Languages.objects.get(url=language_url)
    category = Categories.objects.get(url=category_url, language=language)

    # Check if the category is a direct child of the specified language
    subcategory = None

    if subcategory_url:
        # If a subcategory URL is present, get the subcategory and its tags
        subcategory = category.sub_categories.filter(url=subcategory_url).first()
        if subcategory:
            # Get the common tags for the category and subcategory
            tags_category = category.tags.all()
            tags_subcategory = subcategory.tags.all()
            common_tags = tags_category.filter(id__in=tags_subcategory)
            
            # Get all the records for the common tags, category, and subcategory
            records = Anekdots.objects.filter(tags__in=common_tags, tags__categories=category, tags__categories__sub_categories=subcategory).distinct()
        else:
            common_tags = None
            records = None
    else:
        # If no subcategory URL is present, get the category's tags
        common_tags = category.tags.all()
        records = Anekdots.objects.filter(tags__in=common_tags, tags__categories=category).distinct()

    if subcategory_url and not subcategory:
        raise Http404(f"Subcategory '{subcategory_url}' not found in category '{category_url}'")
    subcategory_url = subcategory.url if subcategory else None
    # Pass the data to the template and render it
    context = {
        'language': language,
        'category': category,
        'subcategory': subcategory,
        'common_tags': common_tags,
        'records': records,
        'subcategory_url': subcategory_url,
    }
    # return JsonResponse(data)
    return render(request, 'anekdoty/category.html', context)



def tags(request, language_url, category_url, subcategory_url=None, tag_url=None, subtag_url=None):
    # Get the language, category, and subcategory based on the language URL, category URL, and subcategory URL
    language = Languages.objects.get(url=language_url)
    category = Categories.objects.get(url=category_url, language=language)
    subcategory = None
    if subcategory_url:
        subcategory = category.sub_categories.filter(url=subcategory_url).first()
    
    # Get the tag and subtag based on the tag URL and subtag URL
    tag = None
    subtag = None
    if tag_url:
        tag = Tags.objects.get(url=tag_url, language=language)
        if subtag_url:
            # check if subtag exists and it is common with the category and tag
            subtag = tag.sub_tags.filter(url=subtag_url).first()
            if not subtag:
                raise Http404("Subtag not found")
    
    # Get the records based on the tag, subtag, category, and subcategory (if present)
    records = None
    if tag:
        records = Anekdots.objects.filter(tags=tag)
        if subtag:
            records = records.filter(tags=subtag)
    elif category:
        common_tags = category.tags.all()
        if subcategory:
            # check if subcategory is common with the category and tag (if present)
            sub_tags = subcategory.tags.all()
            if tag:
                sub_tags = sub_tags.filter(tags__in=[tag])
                common_tags = common_tags.intersection(sub_tags)
            records = Anekdots.objects.filter(tags__in=common_tags)
        if subcategory:
            records = records.filter(tags__categories__sub_categories=subcategory)
    
    # Pass the data to the template and render it
    context = {
        'language': language,
        'category': category,
        'subcategory': subcategory,
        'tag': tag,
        'subtag': subtag,
        'records': records,
        'current_tag': tag,
    }

    return render(request, 'anekdoty/tags.html', context)




def tag_info(request, tag_slugs, lang_slug):
    # split tag slugs by '/'
    tag_slugs = tag_slugs.split('/')

    tag_slugs = tag_slugs[:2]
    # get the last tag slug from the list
    current_tag_slug = tag_slugs[-1]

    # Get the language object based on its slug
    languages_data = get_object_or_404(Languages, url=lang_slug)

    # get the current tag object
    current_tag = get_object_or_404(Tags, language=languages_data, url=current_tag_slug)

    # get the parent tag object for the current tag
    parent_tag = current_tag.parent_tag

    # get all child tags for the parent tag
    child_tags = Tags.objects.filter(Q(parent_tag=current_tag) | Q(pk=current_tag.pk))

    # filter Anekdots by the current tag and its child tags
    anekdots = Anekdots.objects.filter(tags__in=child_tags, language=languages_data).distinct()

    # build breadcrumb links for parent tags
    breadcrumbs = []
    for i, slug in enumerate(tag_slugs[:-1]):
        tag = get_object_or_404(Tags, language=languages_data, url=slug)
        breadcrumbs.append((tag.breadcrumb, f"/{languages_data.url}/{'/'.join(tag_slugs[:i+1])}"))

    # add current tag to breadcrumbs
    breadcrumbs.append((current_tag.breadcrumb, None))

    context = {
        'current_tag': current_tag,
        'parent_tag': parent_tag,
        'child_tags': child_tags,
        'anekdots': anekdots,
        'breadcrumbs': breadcrumbs,
        'languages': languages_data,
        'tag_description': current_tag.description,
        'parent_tag_name': parent_tag.name if parent_tag else None,
        'child_tag_names': [tag.name for tag in child_tags] if child_tags else None,
    }

    # load the anekdoty/anekdot_tag.html template
    template = loader.get_template('anekdoty/anekdot_tag.html')

    # render the template with the context
    rendered_template = template.render(context, request)

    # return the rendered template as an HTTP response
    return HttpResponse(rendered_template)



def breadcrumb(request, slug, lang_url):
    # Get the language object based on its slug
    languages_data = Languages.objects.get(url=lang_url)

    # Get the tag object based on its slug and language
    tags_data = Tags.objects.filter(language=languages_data).order_by('id').get(url=slug)

    # Build the breadcrumb list
    breadcrumb_list = []
    parent_tag = tags_data.parent_tag
    while parent_tag:
        breadcrumb_list.append((parent_tag.name, reverse('tag_info', args=[parent_tag.get_url_path(lang_url), lang_url])))
        parent_tag = parent_tag.parent_tag
    breadcrumb_list.reverse()
    breadcrumb_list.append((tags_data.name, None))
    # Build the BreadcrumbList schema
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": item[0],
                "item": item[1] if item[1] else request.build_absolute_uri(),
            }
            for i, item in enumerate(breadcrumb_list)
        ]
    }

    # Render the breadcrumb template with the breadcrumb list and schema
    context = {
        'breadcrumb_list': breadcrumb_list,
        'schema': schema,
        'languages': languages_data,
        }
    
    return JsonResponse(data)
    # template = loader.get_template('includes/breadcrumb.html')
    # return HttpResponse(template.render(context, request))

