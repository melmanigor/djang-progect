from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import SignUpForm,LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_backends
from .forms import SignUpForm
# Create your views here.
class SignupView(SuccessMessageMixin,CreateView):
    """
    View for user registration using a Django form.

    - Displays a signup form.
    - On valid submission, creates a user, logs them in, and redirects to vacation list.
    """
    form_class = SignUpForm
    template_name = 'user/signup.html'
    success_url = reverse_lazy('vacation_list')
    success_message = "Account created successfully"
    def form_valid(self, form: SignUpForm)->any:
        """
        Called when a valid form is submitted.

        Logs the user in after creating the account by manually setting the auth backend.

        Args:
            form (SignUpForm): The validated signup form.

        Returns:
            HttpResponse: A redirect response to the success URL.
        """
        response = super().form_valid(form)
        backend = get_backends()[0]
        self.object.backend = f"{backend.__module__}.{backend.__class__.__name__}"
        login(self.request, self.object)
        return response

class LoginView(SuccessMessageMixin,LoginView):
    """
    View for user login using Django's built-in LoginView.

    - Displays the login form.
    - On success, logs the user in and shows a success message.
    """
    form_class = LoginForm
    template_name = 'user/login.html'
    success_message = "Logged in successfully"

class LogoutView(LogoutView):
    """
    Logs the user out and redirects them to the home page.

    Uses Django's built-in LogoutView and sets `next_page` as the redirect destination.
    """
    next_page = reverse_lazy('home')    

