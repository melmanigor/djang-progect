from django.contrib.auth import authenticate
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder
from crispy_forms.layout import Div


class SignUpForm(UserCreationForm):
    """
    Form for registering a new user, extending Django's built-in UserCreationForm.
    Includes additional fields and validation for unique email.
    """
    email : forms.EmailField=forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs)->None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset('Sign Up',
                'username',
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2',
                
            ),
            ButtonHolder(
               Div( Submit('submit', 'Sign Up', css_class='btn btn-success'),css_class='text-center')
            )
        )
    def clean_email(self)->str:
        """
        Validate that the provided email does not already exist in the system.
        """
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

class LoginForm(forms.Form):
    """
    Custom login form authenticating via email and password.
    """
    email: forms.EmailField = forms.EmailField(label='Email')
    password: forms.CharField = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset('Login', 'email', 'password'),
            Div(Submit('submit', 'Login', css_class='btn btn-primary'), css_class='text-center')
        )

    def clean(self)->dict:
        """
        Validate email and password using Django's authenticate function.
        """
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            self.user = authenticate(self.request, email=email, password=password)
            if self.user is None:
                raise forms.ValidationError("Email or password is incorrect.")
        return cleaned_data

    def get_user(self)->User:
        """
        Return the authenticated user after clean() runs.
        """
        return self.user
