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

admin.site.register(CustomUser, CustomUserAdmin)
