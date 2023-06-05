import re
from django import template
from django.template.defaultfilters import urlize
from category_default.models import Tags
from django.utils.encoding import smart_str
from django.utils.safestring import mark_safe
from bs4 import BeautifulSoup
import bleach
from django.urls import reverse
from category_default.models import *

register = template.Library()



from django.urls import reverse

from django.urls import reverse

@register.filter
def auto_link(text, category, current_tag=None):
    # Clean the input text to remove any unwanted HTML tags
    clean_text = bleach.clean(text, tags=[], attributes={}, strip=True)

    # Query the Tags model for the list of keywords and their corresponding URLs
    keywords = {}
    for tag in category.tags.all():
        for keyword in tag.seo_keywords.split(','):
            keywords[keyword.strip()] = reverse('category_default:category_tag', kwargs={
                'language_url': category.language.url,
                'category_url': category.url,
                'tag_url': tag.url
            })

    # Create a regular expression pattern to match the keywords
    pattern = re.compile('|'.join(map(re.escape, keywords.keys())))

    # Replace the matched keywords with hyperlinks
    def replace(match):
        keyword = match.group(0)
        if current_tag and keyword.lower() in current_tag.seo_keywords.lower().split(','):
            return keyword
        else:
            # Split the keyword by commas
            parts = keyword.split(',')
            if len(parts) > 2:
                # Limit the parts to the first two
                parts = parts[:2]
            
            # Join the parts back together and replace the keyword with the URL
            new_keyword = ','.join(parts)
            return f'<a href="{keywords.get(keyword, "#")}">{new_keyword}</a>'

    linked_text = pattern.sub(replace, clean_text)
    return mark_safe(linked_text)

# @register.filter
# def auto_link_subcategory(text, category):
#     for subcategory in category.sub_categories.all():
#         for tag in subcategory.tags.all():
#             if tag.seo_keywords:
#                 keywords = {}
#                 for keyword in tag.seo_keywords.split(','):
#                     url_kwargs = {
#                         'language_url': category.language.url,
#                         'category_url': category.url,
#                         'subcategory_url': subcategory.url,
#                         'tag_url': tag.url,
#                     }
#                     # swap category and subcategory URL kwargs
#                     url_kwargs['category_url'], url_kwargs['subcategory_url'] = url_kwargs['subcategory_url'], url_kwargs['category_url']
#                     url = reverse('category_default:tag', kwargs=url_kwargs).replace('/subcategory/', '/subcategory_tag/')
#                     keywords[keyword.strip()] = url
#                 for keyword, url in keywords.items():
#                     text = re.sub(r'\b%s\b' % keyword, '<a href="%s">%s</a>' % (url, keyword), text)
#     return text

@register.filter
def auto_link_subcategory(text, tag, category=None, subcategory=None):
    processed_keywords = set()  # Track processed keywords

    if category is None:
        categories = Categories.objects.filter(tags=tag)

        if categories.exists():
            for category in categories:
                subcategories = category.sub_categories.all()

                for subcategory in subcategories:
                    url = f"/language-set/{category.language.url}/{category.url}/{subcategory.url}/{tag.url}/"

                    if tag.only_subtag and tag.sub_tags.exists():
                        url = f"{url}{tag.sub_tags.first().url}/"

                    keywords = {}
                    if tag.seo_keywords:
                        for keyword in tag.seo_keywords.split(','):
                            keyword = keyword.strip()
                            if keyword not in processed_keywords:  # Skip already processed keywords
                                processed_keywords.add(keyword)
                                keywords[keyword] = url

                    for keyword, url in keywords.items():
                        text = re.sub(r'\b%s\b' % keyword, '<a href="%s">%s</a>' % (url, keyword), text)
    else:
        url = f"/language-set/{category.language.url}/{category.url}/{subcategory.url}/{tag.url}/"

        if tag.only_subtag and tag.sub_tags.exists():
            url = f"{url}{tag.sub_tags.first().url}/"

        keywords = {}
        if tag.seo_keywords:
            for keyword in tag.seo_keywords.split(','):
                keyword = keyword.strip()
                if keyword not in processed_keywords:  # Skip already processed keywords
                    processed_keywords.add(keyword)
                    keywords[keyword] = url

        for keyword, url in keywords.items():
            text = re.sub(r'\b%s\b' % keyword, '<a href="%s">%s</a>' % (url, keyword), text)

    return text




















