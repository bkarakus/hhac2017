from django.contrib import admin

# Register your models here.
from payments.models import Payment, Title

class TitleAdmin(admin.ModelAdmin):
    list_display = ('aciklama_tr', 'aciklama_en', 'fee')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'title', 'orginization', 'email', 'phone', 'status',)
    list_filter = ('title', 'status')
    readonly_fields = ('token', )

admin.site.register(Title, TitleAdmin)
admin.site.register(Payment, PaymentAdmin)