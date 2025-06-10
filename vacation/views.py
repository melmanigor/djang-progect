from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, View, UpdateView,FormView
from .models import Vacation, Country
from .forms import VacationCreateForm, VacationForm, VacationUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
class VacationListView(ListView):
    model = Vacation
    template_name = 'vacation/vacation_list.html'
    context_object_name = 'vacations'
    def get_queryset(self):
        queryset = super().get_queryset()
        country_id = self.request.GET.get('country')
        if country_id:
            queryset = queryset.filter(country__id=country_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countries'] = Country.objects.all()
        return context



class VacationCreateView(SuccessMessageMixin, UserPassesTestMixin, CreateView):
    model = Vacation
    form_class = VacationCreateForm
    template_name = 'vacation/add_vacation.html'
    success_message = "Vacation created successfully"
    success_url = reverse_lazy('vacation_list')

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def test_func(self):
        return self.request.user.is_superuser


class LikeToggleView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        vacation = get_object_or_404(Vacation, pk=pk)
        user = request.user
        if user in vacation.liked_by.all():
            vacation.liked_by.remove(user)
        else:
            vacation.liked_by.add(user)
        return redirect('vacation_list')


class VacationUpdateView(UserPassesTestMixin, UpdateView):
    model = Vacation
    form_class = VacationUpdateForm
    template_name = 'vacation/update_vacation.html'
    success_url = reverse_lazy('vacation_list')

    def form_valid(self, form):
        messages.success(self.request, 'Vacation updated successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def test_func(self):
        return self.request.user.is_superuser


def delete_vacation(request, pk):
    vacation = get_object_or_404(Vacation, pk=pk)

    if request.method == 'POST':
        vacation.delete()
        messages.success(request, f'Vacation in {vacation.country.name} was deleted successfully.')
        return redirect('vacation_list')

    return render(request, 'vacation/delete_vacation.html', {'object': vacation})

class VacationSearchView(FormView):
    
    form_class = VacationForm
    template_name = 'vacation/vacation_search.html'
    

    def form_valid(self, form):
        country = form.cleaned_data['country']
        vacations = Vacation.objects.filter(country=country)
        return self.render_to_response(self.get_context_data(form=form, vacations=vacations))