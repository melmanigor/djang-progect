from django.urls import path
from .views import VacationListApiView,VacationUpdateApiView,CountryListApiView,LikeToggleView,UserSignUpView,LoginAPIView,LogoutAPIView,MeAPIView

urlpatterns = [
    path('vacations/', VacationListApiView.as_view(), name='api-vacation-list'),
    path('vacations/<int:pk>/', VacationUpdateApiView.as_view(), name='api-vacation-update'),

    path('vacations-api/<int:pk>/like/', LikeToggleView.as_view(), name='like-toggle'),
    path('countries-api/', CountryListApiView.as_view(), name='api-country-list'),
    path('signup-api/', UserSignUpView.as_view(), name='signup_api'),
    path('login-api/', LoginAPIView.as_view(), name='login_api'),
    path('logout-api/', LogoutAPIView.as_view(), name='logout_api'),
    path('me-api/', MeAPIView.as_view(), name='me_api'),
]