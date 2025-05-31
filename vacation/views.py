from django.shortcuts import render
from .models import Vacation

# Create your views here.
def vacation_list(request):
    vacations = Vacation.objects.all()
    return render(request, 'vacation_list.html', {'vacations': vacations})
