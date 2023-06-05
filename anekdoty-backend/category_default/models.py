from audioop import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from ckeditor.fields import RichTextField
from django.db import models


# Create your models here.
class Anekdots(models.Model):
    language = models.ForeignKey('directory.Languages', on_delete=models.CASCADE)
    category = models.ManyToManyField('Categories', blank='True')
    tags = models.ManyToManyField('Tags', blank=True, related_name='anekdots_tags')
    h2 = models.CharField(max_length=255, blank=True)
    text = RichTextField(default=True,blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True, default=0)
    date_created = models.DateField(auto_now_add=True, blank=True, null=True)
    date_modified = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.h2

    class Meta:
        managed = True
        db_table = 'anekdots'
        verbose_name_plural = 'Records'


class Tags(models.Model):
    name = models.CharField(max_length=255, unique=True)
    language = models.ForeignKey('directory.Languages', on_delete=models.CASCADE)
    sub_tags = models.ManyToManyField('self', blank=True)
    description = models.TextField(blank=True, null=True)
    seo_title = models.CharField(max_length=255)
    seo_description = models.TextField(blank=True, null=True)
    seo_h1 = models.CharField(max_length=255, blank=True, null=True)
    seo_keywords = models.CharField(max_length=255, blank=True, null=True)
    breadcrumb = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.ImageField(upload_to='tags', verbose_name='Image')
    records_per_page = models.IntegerField(default=20, validators=[MinValueValidator(5), MaxValueValidator(50)])
    parsing_words = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    only_subtag = models.BooleanField(default=False)
    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('categoty_default:tag', kwargs={'lang_url': self.language, 'slug': self.slug})

    def get_absolute_url(self):
        kwargs = {
            'language_url': self.language.url,
            'category_url': self.categories.first().url,  # Assuming each tag has at least one category
            'subcategory_url': '',  # Set the subcategory URL accordingly
            'tag_url': self.url,
        }

        if self.sub_tags.exists():
            subtag = self.sub_tags.first()
            kwargs['subcategory_url'] = subtag.categories.first().url
            kwargs['tag_url'] = subtag.url

            return reverse('sub_tags', kwargs=kwargs)
        else:
            return reverse('tags', kwargs=kwargs)

    class Meta:
        managed = True
        db_table = 'tags'
        verbose_name_plural = 'Tags'


class Categories(models.Model):
    name = models.CharField(max_length=45, null=True)
    sub_categories = models.ManyToManyField('self', blank=True, symmetrical=False)
    language = models.ForeignKey('directory.Languages', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tags', blank=True)
    url = models.CharField(max_length=45)
    description = RichTextField()
    image_url = models.ImageField(upload_to='category', verbose_name='Image')
    seo_title = models.CharField(max_length=45)
    seo_description = models.TextField(blank=True, null=True)
    seo_h1 = models.CharField(max_length=45, blank=True, null=True)
    shown_in_menu = models.BooleanField(default=False)
    behave_as_tag = models.BooleanField(default=False)
    # date_created = models.DateField(auto_now_add=True, blank=True, null=True)
    # date_modified = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'categories'
        verbose_name_plural = 'Categories'
