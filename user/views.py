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
# Create your views here.
class SignupView(SuccessMessageMixin,CreateView):
    form_class = SignUpForm
    template_name = 'user/signup.html'
    success_url = reverse_lazy('vacation_list')
    success_message = "Account created successfully"
    def form_valid(self, form):
        response = super().form_valid(form)
        backend = get_backends()[0]
        self.object.backend = f"{backend.__module__}.{backend.__class__.__name__}"
        login(self.request, self.object)
        return response

class LoginView(SuccessMessageMixin,LoginView):
    form_class = LoginForm
    template_name = 'user/login.html'
    success_message = "Logged in successfully"

class LogoutView(LogoutView):
    next_page = reverse_lazy('home')    

