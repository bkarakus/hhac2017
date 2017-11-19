# -*- coding: utf-8 -*-
__date__ = "13 Ara 2013"

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import File, Image, Menu, Sayfa

class FileAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'title', 'updated',)
    date_hierarchy = 'updated'
    search_fields = ('title', )
    
class ImageAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'title', 'get_size', 'updated', 'sira',)
    list_filter = ('slideshow',)
    list_editable = ('sira',)
    date_hierarchy = 'updated'
    search_fields = ('title', )
    readonly_fields = ('width', 'height',)
    fieldsets = (
        (None, {'fields': ('image', 'title','slideshow')}),
        (_('Size'), {'classes': ('collapse',), 'fields': ('width', 'height',)}),
    )
    
class MenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',),}

class SayfaAdmin(admin.ModelAdmin):
    list_display = ('title_tr','sira','aktif','menu')
    list_editable = ('sira','aktif','menu',)
    prepopulated_fields = {'slug':('title_tr',),}
    list_filter = ('menu',)
    
    class Media:
        js = ('js/tiny_mce/tiny_mce.js',
              'js/tiny_mce/textareas.js',
              'mce_filebrowser/js/filebrowser_init.js',
              )
        
    fieldsets = (
        (None, {
            'fields': ('menu', 'title_tr', 'slug' , 'content_tr', 'sira')
        }),
        ('English', {
            'fields': ('title_en', 'content_en',),
            # 'classes': ('collapse',),
        }),
        ('Yönlendir', {
            # 'classes': ('collapse',),
            'fields': ('url',)
        }),
    )

admin.site.register(File, FileAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Sayfa, SayfaAdmin)
