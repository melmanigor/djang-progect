from django.urls import path
from . import views

urlpatterns = [
    path('', views.vacation_list, name='vacation_list'),
]