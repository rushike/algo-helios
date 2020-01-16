from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model
from django import forms

class AlgonautsSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    contact = forms.RegexField(regex=r'^\d{10}$')
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        field_order = [ 'first_name', 'last_name', 'email', 'contanct' 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].label = 'First Name'
        self.fields["first_name"].widget.attrs["placeholder"] = "First Name"
        self.fields["last_name"].label = 'Last Name'
        self.fields["last_name"].widget.attrs["placeholder"] = "Last Name"
        self.fields["email"].label = 'Email'
        self.fields["email"].widget.attrs["placeholder"] = "Email"
        self.fields["contact"].label = 'Contact'
        self.fields["contact"].widget.attrs["placeholder"] = "Contact Number"
        self.fields["password1"].label = 'Password'
        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password2"].label = 'Confirm'
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm Password"

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user