from django.urls import reverse_lazy
from django.contrib import messages
from .forms import SendEmailForm
from .models import CustomUser
from django.views.generic.edit import FormView
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.


IsStaff = CustomUser.objects.filter(is_staff=True)
# IsStaff = s.is_staff=True

class SendUserEmails(FormView):
    template_name = 'admin/send_email.html'
    form_class = SendEmailForm
    success_url = reverse_lazy('admin:usermetrics_customuser_changelist')

    @staff_member_required
    def form_valid(self, form):
        users = form.cleaned_data['customusers']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        email_users.delay(users, subject, message)
        user_message = '{0} users emailed successfully!'.format(form.cleaned_data['customusers'].count())
        messages.success(self.request, user_message)
        return super(SendUserEmails, self).form_valid(form)