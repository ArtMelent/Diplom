from django.conf import settings
from django.conf.urls import include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, re_path
from django.utils.translation import gettext_lazy as _
from .views import *
from . import views

admin.autodiscover()

app_name = 'category_default'

urlpatterns = [
    path('api/<path>/', views.NotFoundAPIView.as_view(), name='not_found_data'),
    path('api/<str:langUrl>/', views.LanguageDataAPIView.as_view(), name='language_data'),
    path('api/<str:language_url>/<str:category_url>/', CategoryDataAPIView.as_view()),
    path('api/<str:language_url>/<str:category_url>/<str:subcategory_url>/', CategoryDataAPIView.as_view()),
    path('api/<str:language_url>/<str:category_url>/<str:subcategory_url>/<str:tag_url>/', TagsAPIView.as_view()),
    path('api/<str:language_url>/<str:category_url>/<str:subcategory_url>/<str:tag_url>/<str:subtag_url>/', TagsAPIView.as_view()),
    path('api/category/shared-data/for/me/url', CategorySharedDataAPIView.as_view(), name='category-shared-data'),



    path('language-set/<str:url>/', views.language_set, name='language_set'),
    path('language-set/<str:language_url>/<str:category_url>/', views.category, name='categories'),
    path('language-set/<str:language_url>/<str:category_url>/<str:subcategory_url>/', views.category, name='sub_categories'),
    path('language-set/<str:language_url>/<str:category_url>/<str:subcategory_url>/<str:tag_url>/', views.tags, name='tags'),
    path('language-set/<str:language_url>/<str:category_url>/<str:subcategory_url>/<str:tag_url>/<str:subtag_url>/', views.tags, name='sub_tags'),

    # path('<slug:lang_slug>/<slug:tag_slugs>/', tag_info, name='tag_info'),
    # path('<slug:lang_url>/breadcrumb/<slug:slug>/', breadcrumb, name='breadcrumb'),
]