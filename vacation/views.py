from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import Vacation
from .forms import VacationCreateForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.
class VacationListView(LoginRequiredMixin,ListView):
    model = Vacation
    template_name = 'vacation/vacation_list.html'
    context_object_name = 'vacations'
    login_url='login'



class VacationCreateView(UserPassesTestMixin, CreateView):
    model = Vacation
    form_class = VacationCreateForm
    template_name = 'vacation/add_vacation.html'
    success_url = reverse_lazy('vacation_list')
    def form_invalid(self, form):
        print(form.errors)  
        return super().form_invalid(form)

    def test_func(self):
        return self.request.user.is_superuser
