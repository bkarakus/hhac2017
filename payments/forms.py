# encoding: utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _

#from simplemathcaptcha.fields import MathCaptchaField

from payments.models import Payment, PAYMENT_WAITING

class PaymentForm(forms.ModelForm):
    #captcha = MathCaptchaField()
    class Meta:
        model = Payment
        exclude = ('status', 'customer_ip_address', 'fee', 'token', 'created', 'modified')
        
class PaymentEmailForm(forms.Form):
    email = forms.EmailField(label=_('Email'))
    
    def clean(self):
        cleaned_data = super(PaymentEmailForm, self).clean()
        email = cleaned_data.get('email', None)
        try:
            payment = Payment.objects.get(email=email)
        except:
            raise forms.ValidationError(_(u'Please register before payment'))
        else:
            if payment.status != PAYMENT_WAITING:
                raise forms.ValidationError(_(u'your payment was confirmed before'))
            else:
                self.payment = payment