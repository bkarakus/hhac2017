from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ihmc.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', 'pages.views.index', name="index"),
    url(r'^page/(?P<slug>.*)$','pages.views.page_detail', name="page_detail"),
    url(r'^filebrowser/', include('pages.urls')),
    url(r'^payment/', include('payments.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
