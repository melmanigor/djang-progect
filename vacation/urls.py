from django.urls import path
from .views import VacationListView, VacationCreateView

urlpatterns = [
    path('', VacationListView.as_view(), name='vacation_list'),
    path('add/', VacationCreateView.as_view(), name='add_vacation'),
]