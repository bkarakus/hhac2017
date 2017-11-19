# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
__date__ = "24 Ara 2013"

import os

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.files.images import get_image_dimensions
from django.template.defaultfilters import slugify
from django.contrib.flatpages.models import FlatPage

from common.meta import Translate, LocalizeModelBase

def rename_file(value):
    filename, ext = os.path.splitext(value)
    filename = slugify(filename)
    return "%s%s" % (filename,ext)

class Menu(models.Model):
    title = models.CharField(_(u'Menu Adı'), max_length=20)
    slug = models.SlugField()
    
    class Meta:
        verbose_name = _(u'Menu')
        verbose_name_plural = _(u'Menuler')
        
    def __unicode__(self):
        return self.title

class Sayfa(models.Model):
    __metaclass__ = LocalizeModelBase
    
    menu = models.ForeignKey(Menu, blank=True,null=True)   
    title_tr = models.CharField(_(u'Başlık'), max_length=100)
    title_en = models.CharField(_(u'Başlık'), max_length=100, blank=True, null=True)
    title = Translate
    
    content_tr = models.TextField(_(u'İçerik'), blank=True,null=True)
    content_en = models.TextField(_(u'İçerik'), blank=True,null=True)
    content = Translate 
    
    slug = models.SlugField()
    
    url = models.CharField(_('URL'), max_length=100, blank=True, null=True)
    
    aktif = models.BooleanField(default=True)
    sira = models.IntegerField(_(u'Sıra'), default=100)
    
    def get_absolute_url(self):
        url = reverse('page_detail', kwargs={'slug':self.slug})
        return url
    
    class Meta:
        verbose_name = _(u'Sayfa')
        verbose_name_plural = _(u'Sayfalar')
        ordering = ('sira',)
    
    def __unicode__(self):
        return self.title

class Image(models.Model):
    def get_file_path(self, filename):
        upload_to = os.path.join(settings.IMAGES_DIR, rename_file(filename))
        return upload_to
    
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    image = models.ImageField(_('image'), upload_to=get_file_path, max_length=255)
    title = models.CharField(_('title'), max_length=255, null=True, blank=True)
    slideshow = models.BooleanField(_(u"Slideshow'da göster"), default=False)
    sira = models.IntegerField(_(u'Sıra'), default=100)
    width = models.IntegerField(_('width'), blank=True, null=True)
    height = models.IntegerField(_('height'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('resim')
        verbose_name_plural = _('resimler')
        ordering = ('sira',)
        
    def __unicode__(self):
        return self.image.name
    
    def save(self, *args, **kwargs):
        existing_images = Image.objects.filter(image=os.path.join(settings.IMAGES_DIR, self.image.name))
        for existing_image in existing_images:
            existing_image.delete()
            
        self.get_image_information()
        super(Image, self).save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        self.image.storage.delete(self.image.name)
        super(Image, self).delete(*args, **kwargs)
    
    def get_filename(self):
        return os.path.basename(self.image.name)
        
    def get_image_information(self):
        self.width, self.height = get_image_dimensions(self.image) or (0, 0)
        if not self.title:
            self.title = self.get_filename()
    
    def get_size(self):
        return '%s x %s' % (self.width, self.height)
    get_size.short_description = _('Size')
    
class File(models.Model):
    def get_file_path(self,filename):
        upload_to = os.path.join(settings.FILES_DIR,rename_file(filename))
        return upload_to
    
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    file = models.FileField(_('file'), upload_to=get_file_path, max_length=255)
    title = models.CharField(_('title'), max_length=255, null=True, blank=True)
        
    class Meta:
        verbose_name = _('dosya')
        verbose_name_plural = _('dosyalar')
        ordering = ('-updated', )

    def __unicode__(self):
        return self.file.name

    def save(self, *args, **kwargs):
        # delete existing File(s) with the same file.name - TODO: warn about this?
        existing_files = File.objects.filter(file=os.path.join(settings.FILES_DIR, self.file.name))
        for existing_file in existing_files:
            existing_file.delete()
            
        self.get_file_information()
        super(File, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file.storage.delete(self.file.name)
        super(File, self).delete(*args, **kwargs)
        
    def get_filename(self):
        return os.path.basename(self.file.name)
    
    def get_file_information(self):
        if not self.title:
            self.title = self.get_filename()
