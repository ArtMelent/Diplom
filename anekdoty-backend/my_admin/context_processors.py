from category_default.models import Tags
from directory.models import Languages


def add_variable_to_context(request):
    language_name = Languages.objects.values_list('name', 'id')
    language = Languages.objects.all().values_list('name', 'id')

    context = {
        'testme': 'Hello world!',
        'lang_id': language,
        'lang_name': language_name
    }
    return context



