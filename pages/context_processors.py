from django.contrib.sites.models import Site, RequestSite
from django.contrib.auth.forms import AuthenticationForm

def site(request):
    if Site._meta.installed:
        site = Site.objects.get_current()
    else:
        site = RequestSite(request)
    context = {
        'site': site,
        'login_form': AuthenticationForm(),
    }
    return context