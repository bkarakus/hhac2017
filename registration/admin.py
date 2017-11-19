from django.contrib import admin
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import ugettext_lazy as _

from registration.models import RegistrationProfile, User
from registration.models import Title

class TitleAdmin(admin.ModelAdmin):
    list_display = ["aciklama_tr", "aciklama_en"]

class UserAdmin(AuthUserAdmin):
    readonly_fields = ('last_login', 'date_joined',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('title', 'first_name', 'last_name', 'email', 'university', 'department', 'address', 'phone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
        (_('Personal info'), {'fields': ('title', 'first_name', 'last_name', 'email', 'university', 'department', 'address', 'phone')}),
        
    )

class RegistrationAdmin(admin.ModelAdmin):
    actions = ['activate_users', 'resend_activation_email']
    list_display = ('user', 'activation_key_expired')
    raw_id_fields = ['user']
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

    def activate_users(self, request, queryset):
        """
        Activates the selected users, if they are not alrady
        activated.
        
        """
        for profile in queryset:
            RegistrationProfile.objects.activate_user(profile.activation_key)
    activate_users.short_description = _("Activate users")

    def resend_activation_email(self, request, queryset):
        """
        Re-sends activation emails for the selected users.

        Note that this will *only* send activation emails for users
        who are eligible to activate; emails will not be sent to users
        whose activation keys have expired or who have already
        activated.
        
        """
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        for profile in queryset:
            if not profile.activation_key_expired():
                profile.send_activation_email(site)
    resend_activation_email.short_description = _("Re-send activation emails")


admin.site.register(RegistrationProfile, RegistrationAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Title, TitleAdmin)
