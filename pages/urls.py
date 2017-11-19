try:
    from django.conf.urls.defaults import patterns, url
except ImportError:
    from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^image/$', 
        views.filebrowser, 
        {'file_type': 'img'},
        name='mce-filebrowser-images'
    ),
    url(r'^file/$', 
        views.filebrowser, 
        {'file_type': 'doc'},
        name='mce-filebrowser-documents'
    ),
)