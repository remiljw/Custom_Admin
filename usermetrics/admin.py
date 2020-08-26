from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm 
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.urls import reverse, path
from django.conf.urls import url
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
# Register your models here. 

admin.site.unregister(Group)

class CustomUserAdmin(UserAdmin):    
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username','email', 'is_active', 'user_status')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(r'^(?P<customuser_id>.+)/change/$', self.is_active, name='change'),
        ]
        return custom_urls + urls

    def user_status(self, obj):
        return format_html(
            '<a class="button" href="{}"> Deactivate</a>&nbsp;'
            '<a class="button" href="{}"> Reactivate</a>',
            reverse('admin:change', args=[obj.pk]),reverse('admin:change', args=[obj.pk]),
        )
    user_status.allow_tags = True
    user_status.short_description = 'Options'

    def is_active(self, request, customuser_id, *args, **kwrags):
        opt = customuser_id
        user = CustomUser.objects.get(id=opt)
        if user.is_active == True:
            user.is_active=False
            user.save()
        else:
            user.is_active=True
            user.save()
        return HttpResponseRedirect(reverse('../'))
admin.site.register(CustomUser, CustomUserAdmin)
