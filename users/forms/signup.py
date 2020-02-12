from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model
from django import forms

class AlgonautsSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    contact_no = forms.RegexField(regex=r'^\d{10}$')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields["first_name"].label = 'First Name'
        self.fields["first_name"].widget.attrs["placeholder"] = "First Name"
        self.fields["last_name"].label = 'Last Name'
        self.fields["last_name"].widget.attrs["placeholder"] = "Last Name"
        self.fields["email"].label = 'Email'
        self.fields["email"].widget.attrs["placeholder"] = "Email"
        self.fields["contact_no"].label = 'Contact'
        self.fields["contact_no"].widget.attrs["placeholder"] = "Contact Number"
        self.fields["password1"].label = 'Password'
        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password2"].label = 'Confirm'
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm Password"

    def save(self, request):
        user = super(AlgonautsSignupForm, self).save(request)
        profile = user
        profile.first_name = self.cleaned_data['first_name']
        profile.last_name = self.cleaned_data['last_name']
        profile.contact_no = self.cleaned_data['contact_no']

        profile.save()
        return user
        