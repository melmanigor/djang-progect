from django.shortcuts import render
from django.views.generic import ListView
from .models import Vacation

# Create your views here.
class VacationListView(ListView):
    model = Vacation
    template_name = 'vacation/vacation_list.html'