# -*- coding:utf-8 -*-

from django.template import Library, Node, TemplateSyntaxError
from django.utils.translation import ugettext as _

from pages.models import Sayfa, Menu, Image

register = Library()

class PagesNode(Node):
    """
    Get the books and add to the context
    """
    def __init__(self, menu_slug,context_var):
        self.menu_slug = menu_slug
        self.context_var = context_var
        
    def render(self, context):
        try:
            menu = Menu.objects.get(slug=self.menu_slug)
        except Menu.DoesNotExist, Menu.MultipleObjectsReturned:
            pages = []
        else:
            pages = Sayfa.objects.filter(menu=menu,aktif=True)
        context[self.context_var] = pages
        return ''
    
def get_pages(parser, token):
    """
    {% get_pages menu_slug as pages %}
    """
    try:
        bits = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError(
            _('tag requires exactly two arguments'))
    if len(bits) != 4:
        raise TemplateSyntaxError(
            _('tag requires exactly three arguments'))
    if bits[2] != 'as':
        raise TemplateSyntaxError(
            _("first argument to tag must be 'as'"))
    return PagesNode(bits[1],bits[3])

class ImageNode(Node):
    """
    Get the books and add to the context
    """
    def __init__(self, context_var):
        self.context_var = context_var
        
    def render(self, context):
        images = Image.objects.filter(slideshow=True)
        context[self.context_var] = images
        return ''
    
def get_slideshow_images(parser, token):
    """
    {% get_slideshow_images as pages %}
    """
    try:
        bits = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError(
            _('tag requires exactly two arguments'))
    if len(bits) != 3:
        raise TemplateSyntaxError(
            _('tag requires exactly three arguments'))
    if bits[1] != 'as':
        raise TemplateSyntaxError(
            _("first argument to tag must be 'as'"))
    return ImageNode(bits[2])

register.tag('get_pages', get_pages)
register.tag('get_slideshow_images', get_slideshow_images)