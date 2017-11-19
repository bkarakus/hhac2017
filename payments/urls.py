from django.conf.urls import patterns, include, url
from django.conf import settings

from payments.views import PaymentCreateView, PaymentEmailView, process_payment, cancel_payment, pay_now

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ihmc.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(regex = r'^register/$',
        view  = PaymentCreateView.as_view(),
        name  = 'create_payment',
    ),
    url(regex = r'^pay-now-email/$',
        view  = PaymentEmailView.as_view(),
        name  = 'pay_now_email',
    ),
    url(r'^pay-now/$', pay_now,
        name='pay_now'),      
    url(r'^process/$', process_payment,
        name='process_payment'),
    url(r'^cancel/$', cancel_payment,
        name='cancel_payment'),
)
