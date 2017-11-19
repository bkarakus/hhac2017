# -*- coding: utf-8 -*-
__date__ = "25 Ara 2013"

from django import forms

from models import File, Image

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file',)
        
class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image',)