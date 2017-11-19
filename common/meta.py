from django.db.models.base import ModelBase
from django.utils.translation import get_language
from django.conf import settings

__all__ = ('Translate', 'LocalizeModelBase')

Translate = object()

class LocalizeModelBase(ModelBase):
    def __new__(cls, name, bases, attrs):
        for key in attrs.keys():
            if attrs[key] is Translate:
                attrs[key] = make_property(key)
        return super(LocalizeModelBase, cls).__new__(cls, name, bases, attrs)
    
def make_property(k):
    def pget(self):
        value = None
        try:
            value = getattr(self, "%s_%s" % (k, get_language()))
        except AttributeError:
            value = getattr(self, "%s_%s" % (k, settings.LANGUAGE_CODE))
        if value is None or value == '':
            value = getattr(self, "%s_%s" % (k, settings.LANGUAGE_CODE))
        return value
    def pset(self, value):
        try:
            value = setattr(self, "%s_%s" % (k, get_language()), value)
        except AttributeError:
            value = setattr(self, "%s_%s" % (k, settings.LANGUAGE_CODE), value)
    return property(pget, pset)