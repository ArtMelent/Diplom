
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns


from .yasg import urlpatterns as doc_urls
from django.conf.urls.static import static
from directory.urls import *
# from my_admin.context_processors import add_variable_to_context
from my_admin import context_processors
# from wagtail.admin import urls as wagtailadmin_urls
# from wagtail import urls as wagtail_urls
# from wagtail.documents import urls as wagtaildocs_urls
admin.autodiscover()




urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls, name='admin-panel'),
    path('', include('category_default.urls', namespace='category_default')),
    path('', include('my_admin.urls', namespace='my_admin')),
    path('api-auth/', include('rest_framework.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



urlpatterns += doc_urls


urlpatterns += i18n_patterns(
    # prefix_default_language=False,
)
