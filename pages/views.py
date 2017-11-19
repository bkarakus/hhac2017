# -*- coding: utf-8 -*-
__date__ = "25 Ara 2013"

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.utils.translation import ugettext as _
from django.utils import translation
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site, get_current_site
from django.conf import settings

from models import File, Image, Sayfa, Menu
from forms import FileUploadForm, ImageUploadForm

@staff_member_required
def filebrowser(request, file_type):
    template = 'filebrowser.html'
    is_images_dialog = (file_type == 'img')
    is_documents_dialog = (file_type == 'doc')
    uploaded_file = None
    upload_tab_active = False
    if is_documents_dialog:
        upload_form_class = FileUploadForm
        files = File.objects.all()
    else:
        upload_form_class = ImageUploadForm
        files = Image.objects.all()
    
    upload_form = upload_form_class()
       
    if request.POST:
        upload_form = upload_form_class(request.POST, request.FILES)
        upload_tab_active = True
        if upload_form.is_valid():
            uploaded_file = upload_form.save()
            
    data = {
        'files': files,
        'pages': Sayfa.objects.filter(aktif=True),
        'upload_form': upload_form,
        'uploaded_file': uploaded_file,
        'upload_tab_active': upload_tab_active,
        'is_images_dialog': is_images_dialog,
        'is_documents_dialog': is_documents_dialog,
    }
    return render_to_response(template, data, RequestContext(request))

def index(request, template_name='pages/index.html'):
    title = u''
    return render_to_response(template_name, RequestContext(request, {
        'title': title,
    }))
    
def page_detail(request, slug,template_name='pages/page_detail.html'):
    page = get_object_or_404(Sayfa, slug=slug, aktif=True)
    if page.slug == u'kongre-programi':
        template_name='pages/full_page.html'
    
    if page.url:
        return redirect(page.url)
    
    return render_to_response(template_name, RequestContext(request, {
        'title': page.title,
        'show_title': True,
        'page': page,
    }))
    
from django.utils import translation

def set_language(request):
    next = request.REQUEST.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next:
        next = '/'
    response = HttpResponseRedirect(next)
    if request.method == 'GET':
        lang_code = request.GET.get('language', None)
        if lang_code and translation.check_for_language(lang_code):
            if hasattr(request, 'session'):
                request.session['django_language'] = lang_code
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
            translation.activate(lang_code)
    return response
