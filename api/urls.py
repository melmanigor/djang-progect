from django.urls import path
from .views import VacationListApiView,VacationUpdateApiView,CountryListApiView,LikeToggleView

urlpatterns = [
    path('vacations/', VacationListApiView.as_view(), name='api-vacation-list'),
    path('vacations/<int:pk>/update/', VacationUpdateApiView.as_view(), name='api-vacation-update'),

    path('vacations/<int:pk>/like/', LikeToggleView.as_view(), name='like-toggle'),
    path('countries/', CountryListApiView.as_view(), name='api-country-list'),
]