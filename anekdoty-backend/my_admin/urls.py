from django.conf import settings
from django.conf.urls import include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, re_path
from django.utils.translation import gettext_lazy as _
from .views import language_filter, category_default_app
from . import views
from .forms import *
admin.autodiscover()

app_name = 'my_admin'

urlpatterns = [
    path('test/languages/option/', manage_languages, name='manage_languages'),
    path('language/test/work', language_filter, name='language_filter'),
    path('<slug:lang_slug>/admin/category_default', category_default_app, name='category_default_app')

]



# urlpatterns += language_set (

# path('lang_url/<slug:languges>/', languages, name = 'switcher'),
# )