# from django import forms
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .models import CustomUser

# class CustomUserCreationForm(UserCreationForm):

#     class Meta:
#         model = CustomUser
#         fields =('username', 'email')

# class CustomUserChangeForm(UserChangeForm):

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email')

# class SendEmailForm(forms.Form):
#     subject = forms.CharField(
#         widget=forms.TextInput(attrs={'placeholder': _('Subject')}))
#     message = forms.CharField(widget=forms.Textarea)
#     users = forms.ModelMultipleChoiceField(label="To",
#                                            queryset=CustomUser.objects.all(),
#                                            widget=forms.SelectMultiple())