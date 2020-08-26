import json
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.urls import reverse, path
from django.conf.urls import url
from django.http import HttpResponseRedirect, JsonResponse
# Register your models here. 

admin.site.unregister(Group)

class CustomUserAdmin(UserAdmin):    
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username','email', 'is_active',  'date_joined','user_status',)
    ordering=('date_joined',)
    

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = (
            CustomUser.objects.annotate(date=TruncDay("date_joined"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("date")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(r'^(?P<customuser_id>.+)/options/$', self.admin_site.admin_view(self.is_active), name='options'),
            path('chart_data/', self.admin_site.admin_view(self.chart_data_endpoint))
        ]
        return custom_urls + urls

    def chart_data_endpoint(self, request):
        chart_data = self.chart_data()
        return JsonResponse(list(chart_data), safe=False)

    def chart_data(self):
        return (
            CustomUser.objects.annotate(date=TruncDay("date_joined"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("date")
        )

    def user_status(self, obj):
        if obj.is_active == True:
            return format_html('<a class="button" href="{}"> Deactivate</a>',
            reverse('admin:options', args=[obj.pk]))
        else:
            return format_html(
            '<a class="button" href="{}"> Activate</a>',
            reverse('admin:options', args=[obj.pk]))
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
        return HttpResponseRedirect('../../')
admin.site.register(CustomUser, CustomUserAdmin)
