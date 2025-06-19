from typing import Any, Dict
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, View, UpdateView,FormView,DetailView
from .models import Vacation, Country
from .forms import VacationCreateForm, VacationForm, VacationUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse,HttpRequest
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseForbidden


# Create your views here.
class VacationListView(ListView):
    """
    Display a list of vacations, optionally filtered by selected country.
    """
    model = Vacation
    template_name = 'vacation/vacation_list.html'
    context_object_name = 'vacations'
    def get_queryset(self)->Any:
        """
        Returns a filtered queryset of vacations by country (if provided).
        """
        queryset = super().get_queryset().order_by('start_date')
        country_id = self.request.GET.get('country')
        if country_id:
            queryset = queryset.filter(country__id=country_id)
        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Adds list of countries to context.
        """
        context = super().get_context_data(**kwargs)
        context['countries'] = Country.objects.all()
        return context

class VacationCreateView(SuccessMessageMixin, UserPassesTestMixin, CreateView):
    """
    Admin-only view to create a new vacation.
    """
    model = Vacation
    form_class = VacationCreateForm
    template_name = 'vacation/add_vacation.html'
    success_message = "Vacation created successfully"
    success_url = reverse_lazy('vacation_list')

    def form_invalid(self, form: VacationCreateForm)->HttpResponse:
        """
    Handle invalid vacation creation form submission.

    Prints form errors to the console (useful for debugging)
    and returns the standard invalid form response.

    Args:
        form (VacationCreateForm): The invalid form instance.

    Returns:
        HttpResponse: The response with form errors rendered.
    """
        print(form.errors)
        return super().form_invalid(form)

    def test_func(self)->bool:
        """
    Check if the current user is an admin.

    Returns:
        bool: True if the user is an admin, False otherwise.
    """
        return self.request.user.is_superuser


class LikeToggleView(LoginRequiredMixin, View):
    """
    Authenticated users can like/unlike a vacation (admins can't).
    """
    def post(self, request:HttpRequest, pk:int, *args:Any, **kwargs:Any)->HttpResponse:
        if request.user.is_superuser:
            return HttpResponseForbidden("Admins cannot like vacations")
        vacation = get_object_or_404(Vacation, pk=pk)
        user = request.user
        if user in vacation.liked_by.all():
            vacation.liked_by.remove(user)
        else:
            vacation.liked_by.add(user)
        return redirect('vacation_list')


class VacationUpdateView(UserPassesTestMixin, UpdateView):
    """
    Admin-only view to update a vacation.
    """
    model = Vacation
    form_class = VacationUpdateForm
    template_name = 'vacation/update_vacation.html'
    success_url = reverse_lazy('vacation_list')

    def form_valid(self, form: VacationUpdateForm)->HttpResponse:
        """
    Handle valid vacation update form submission.

    Adds a success message to the user and continues with the default processing.

    Args:
        form (VacationUpdateForm): The validated form instance.

    Returns:
        HttpResponse: The redirect response after successful update.
    """
        messages.success(self.request, 'Vacation updated successfully')
        return super().form_valid(form)

    def form_invalid(self, form: VacationUpdateForm)->HttpResponse:
        """
    Handle invalid vacation update form submission.

    Prints form errors to the console and continues with the default invalid form response.

    Args:
        form (VacationUpdateForm): The invalid form instance.

    Returns:
        HttpResponse: The response rendering the form with errors.
    """
        print(form.errors)
        return super().form_invalid(form)


    def test_func(self)->bool:
        """
    Check whether the current user has permission to update vacations.

    Returns:
        bool: True if the user is an admin (superuser), False otherwise.
    """
        return self.request.user.is_superuser


def delete_vacation(request:HttpRequest, pk:int)->HttpResponse:
    """""
    Admin-only function view to delete a vacation.
    """
    if not request.user.is_superuser:
        return HttpResponseForbidden("Admins can delete vacations")
    vacation = get_object_or_404(Vacation, pk=pk)

    if request.method == 'POST':
        vacation.delete()
        messages.success(request, f'Vacation in {vacation.country.name} was deleted successfully.')
        return redirect('vacation_list')

    return render(request, 'vacation/delete_vacation.html', {'object': vacation})

class VacationSearchView(FormView):
    """
    Search vacations by selected country.
    """
    
    form_class = VacationForm
    template_name = 'vacation/vacation_search.html'
    

    def form_valid(self, form: VacationForm)->HttpResponse:
        """
    Handle a valid vacation search form submission.

    Filters vacation objects by the selected country and renders the results
    using the current form and filtered context.

    Args:
        form (VacationForm): The validated search form containing a country.

    Returns:
        HttpResponse: The response with the filtered vacation list rendered in the template.
    """
        country = form.cleaned_data['country']
        vacations = Vacation.objects.filter(country=country)
        return self.render_to_response(self.get_context_data(form=form, vacations=vacations))

class VacationDetailsView(DetailView):
    """
    Display the details of a vacation.
    """
    model = Vacation
    template_name = 'vacation/vacation_details.html'
    context_object_name = 'vacation'

    