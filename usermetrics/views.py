from django.urls import reverse_lazy
from django.contrib import messages
from .forms import SendEmailForm
from .models import CustomUser
from django.views.generic.edit import FormView
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.


class IsStaffMixin(UserPassesTestMixin, LoginRequiredMixin):

    def test_func(self):
        return self.request.user.is_staff

class SendUserEmailsView(IsStaffMixin, FormView):
    template_name = 'admin/send_email.html'
    form_class = SendEmailForm
    success_url = reverse_lazy('admin:usermetrics_customuser_changelist')

    
    def form_valid(self, form):
        users = form.cleaned_data['customusers']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        email_users.delay(users, subject, message)
        user_message = '{0} users emailed successfully!'.format(form.cleaned_data['customusers'].count())
        messages.success(self.request, user_message)
        return super(SendUserEmails, self).form_valid(form)