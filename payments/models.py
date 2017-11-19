# encoding: utf-8
from uuid import uuid4

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from common.meta import LocalizeModelBase, Translate

PAYMENT_WAITING = 'waiting'
PAYMENT_CONFIRMED = 'confirmed'
PAYMENT_REJECTED = 'rejected'
PAYMENT_REFUNDED = 'refunded'

# Create your models here.
PAYMENT_STATUS_CHOICES = (
    (PAYMENT_WAITING, _(u'Waiting for confirmation')),
    (PAYMENT_CONFIRMED, _(u'Confirmed')),
    (PAYMENT_REJECTED, _(u'Rejected')),
    (PAYMENT_REFUNDED, _(u'Refunded')),
)

class Title(models.Model):
    __metaclass__ = LocalizeModelBase
    
    aciklama_tr = models.CharField(u'Açıklama (Kısa)', max_length=50, unique=True)
    aciklama_en = models.CharField(u'Açıklama (Kısa)[En]', max_length=50, blank=True, null=True)
    aciklama = Translate
    
    fee = models.DecimalField(u'Registration Fee', max_digits=9, decimal_places=2, default='0.0')
    
    def __unicode__(self):
        return "%s - %s$" % (self.aciklama, self.fee)
    
    class Meta:
        verbose_name = _('Registration Fee')
        verbose_name_plural = _('Registration Fees')

class Payment(models.Model):
    '''
    Represents a single transaction. Each instance has one or more PaymentItem.
    ''' 
    title = models.ForeignKey(Title, verbose_name=_(u'Registration Type'))
    full_name = models.CharField(_(u'Name-Surname'), max_length=100)
    orginization = models.CharField(_(u'The organization where you work'), max_length=256)
    profession = models.CharField(_(u'Profession'), max_length=100)
    address_1 = models.CharField(_(u'Address Line 1'), max_length=50)
    address_2 = models.CharField(_(u'Address Line 2'), max_length=50, blank=True)
    phone = models.CharField(_(u'Telephone'), max_length=25)
    email = models.EmailField(_(u'Email'), unique=True)
    status = models.CharField(
        max_length=10, choices=PAYMENT_STATUS_CHOICES, default='waiting')
    customer_ip_address = models.GenericIPAddressField(blank=True, null=True, editable=False)
    fee = models.DecimalField(max_digits=9, decimal_places=2)
    token = models.CharField(max_length=36, blank=True, default='')
    #: Creation date and time
    created = models.DateTimeField(auto_now_add=True)
    #: Date and time of last modification
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')

    def save(self, **kwargs):
        if not self.token:
            tries = {}  # Stores a set of tried values
            while True:
                token = str(uuid4())
                if token in tries and len(tries) >= 100:  # After 100 tries we are impliying an infinite loop
                    raise SystemExit('A possible infinite loop was detected')
                else:
                    if not self._default_manager.filter(token=token).exists():
                        self.token = token
                        break
                tries.add(token)
                
        if not self.fee:
            self.fee = self.title.fee

        return super(Payment, self).save(**kwargs)

    def __unicode__(self):
        return self.full_name

    def get_process_url(self):
        return reverse('process_payment', kwargs={'token': self.token})
    
    def get_cancel_url(self):
        return reverse('cancel_payment', kwargs={'token': self.token})