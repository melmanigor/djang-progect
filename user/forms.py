from django.contrib.auth import authenticate
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder
from crispy_forms.layout import Div


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'role']

    def __init__(self, *args, **kwargs):
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
                'role',
            ),
            ButtonHolder(
                Submit('submit', 'Sign Up', css_class='btn btn-success')
            )
        )

class LoginForm(AuthenticationForm):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)  
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset('Login',
                'email',
                'password',
            ),
             Div(
        Submit('submit', 'Login', css_class='btn btn-primary'),
        css_class='text-center'
      
    )
)
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            self.user = authenticate(self.request, email=email, password=password)
            if self.user is None:
                raise forms.ValidationError("Email or password is incorrect.")
        return cleaned_data
