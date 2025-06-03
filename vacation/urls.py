from django.urls import path
from .views import VacationListView, VacationCreateView, LikeToggleView, VacationUpdateView, VacationSearchView
from . import views

urlpatterns = [
    path('', VacationListView.as_view(), name='vacation_list'),
    path('add/', VacationCreateView.as_view(), name='add_vacation'),
    path('<int:pk>/like/', LikeToggleView.as_view(), name='like_vacation'),
    path('<int:pk>/edit/',VacationUpdateView.as_view(),name='update_vacation'),
    path('vacation/<int:pk>/delete/', views.delete_vacation, name='delete_vacation'),
    path('vacation/search/', VacationSearchView.as_view(), name='vacation_search'),

]