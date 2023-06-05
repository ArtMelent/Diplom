from django.forms import modelformset_factory
from django.shortcuts import render
from directory.models import Languages


def manage_languages(request):
    DirectoryFormSet = modelformset_factory(Languages, fields=('name', 'code', 'url'))
    if request.method == 'POST':
        formset = DirectoryFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            # do something.
    else:
        formset = DirectoryFormSet()
    return render(request, 'manage_languages.html', {'formset': formset})
