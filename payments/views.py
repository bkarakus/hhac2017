# encoding: utf-8
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView, FormView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http.response import HttpResponseRedirect

from payments.models import Payment, PAYMENT_CONFIRMED
from payments.forms import PaymentForm, PaymentEmailForm
from common.ipaddr import get_ip

class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentForm
    #fields = ['title', 'full_name', 'orginization', 'profession', 'address_1', 'address_2', 'phone', 'email']
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.customer_ip_address = get_ip(self.request)
        self.object.save()
        self.request.session['payment_token'] = self.object.token
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('pay_now')
    
class PaymentEmailView(FormView):
    template_name = 'payments/email.html'
    form_class = PaymentEmailForm
    
    def get_success_url(self):
        return reverse('pay_now')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        self.request.session['payment_token'] = form.payment.token
        return super(PaymentEmailView, self).form_valid(form)

def pay_now(request):
    try:
        token = request.session['payment_token']
    except:
        token = None
    
    payment = get_object_or_404(Payment, token=token)
    
    process_url = reverse('process_payment')
    cancel_url = reverse('cancel_payment')
    
    context = {
        'RURL': request.build_absolute_uri(process_url),
        'CURL': request.build_absolute_uri(cancel_url),
        'object': payment,
    }
    if payment.status == 'waiting':
        return render(request, 'payments/pay_now.html', context)
    else:
        to = reverse('index')
        return redirect(to)

def process_payment(request):
    '''
    try:
        token = request.session['payment_token']
        del request.session['payment_token']
    except:
        token = None
        
    payment = get_object_or_404(Payment, token=token)
    payment.status = PAYMENT_CONFIRMED
    payment.save()
    '''
    
    to = reverse('index')
    messages.success(request, message=_(u'Payment has been completed'))
    return redirect(to)

def cancel_payment(request):
    to = reverse('pay_now')
    messages.warning(request, message=_(u'Payment canceled'))
    return redirect(to)