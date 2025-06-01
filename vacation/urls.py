from django.urls import path
from .views import VacationListView

urlpatterns = [
    path('', VacationListView.as_view(), name='vacation_list'),
]