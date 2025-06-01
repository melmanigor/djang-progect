from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.
class SignupView(SuccessMessageMixin,CreateView):
    form_class = SignUpForm
    template_name = 'user/signup.html'
    success_url = reverse_lazy('home')
    success_message = "Account created successfully"
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class LoginView(SuccessMessageMixin,LoginView):
    template_name = 'user/login.html'
    success_message = "Logged in successfully"

class LogoutView(LogoutView):
    next_page = reverse_lazy('home')    

