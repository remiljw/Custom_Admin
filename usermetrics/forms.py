from django import forms
from .models import CustomUser

class SendEmailForm(forms.Form):
    subject = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': ('Subject')}))
    message = forms.CharField(widget=forms.Textarea)
    customusers = forms.ModelMultipleChoiceField(label="To",
                                           queryset=CustomUser.objects.all(),
                                           widget=forms.SelectMultiple())