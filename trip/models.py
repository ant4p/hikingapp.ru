from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.urls import reverse
from easy_thumbnails.fields import ThumbnailerImageField

from categories.models import Category

from tags.models import Tag


class Trip(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')
    date = models.DateField(verbose_name=_('Date'))
    title_photo = ThumbnailerImageField(upload_to="photos/%Y/%m/%d/", default=None, blank=True, verbose_name=_('title_photo'))
    content = models.TextField(blank=True, verbose_name=_('Description'))
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Create time')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Update time')
    published = models.BooleanField(verbose_name=_('Status'))

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='categories',
                                 verbose_name=_('Categories'))
    tag = models.ManyToManyField(Tag, blank=True, related_name='tags', verbose_name=_('Tags'))
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='travelers',
                             null=True, default=None)

    class Meta:
        db_table = 'trips'
        ordering = ['-time_create']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('trip', kwargs={'slug': self.slug})
