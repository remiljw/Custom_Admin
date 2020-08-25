from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm 
from django.contrib.auth.models import Group

# Register your models here. 

admin.site.unregister(Group)

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username','email', 'is_active',]
    actions = ['is_not_active','is_active',]

    def is_not_active(self, request, queryset):
        queryset.update(is_active=False)
    is_not_active.short_description = "Deactivate Selected User(s)" 

    def is_active(self, request, queryset):
        queryset.update(is_active=True)
    is_active.short_description = "Reactivate Selected User(s)"

admin.site.register(CustomUser, CustomUserAdmin)
