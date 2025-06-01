from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):
      email=forms.EmailField(required=True)
      class Meta(UserCreationForm.Meta):
           model=User
           fields=['username','email','first_name','last_name','password1','password2','role']

class LoginForm(forms.Form):
      username=forms.CharField(label='Username',required=True,max_length=30)
      password=forms.CharField(label='Password',required=True,widget=forms.PasswordInput)