from django.shortcuts import render
from rest_framework import generics,permissions,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework.generics import get_object_or_404
from django.contrib.auth import login,logout
from vacation.models import Vacation,Country,Like
from .serializers import VacationSerializer,CountrySerializer,LikeSerializer, LoginSerializer,UserSignUpSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import BasePermission
from typing import Type,Any


class IsAdminUserCustom(BasePermission):
    """
    Custom permission to allow access only to authenticated users
    with the role name 'Admin'.

    This is useful when using a custom User model with a related Role model.

    """
     
    def has_permission(self, request, view) -> bool:

        """
        Check if the user is authenticated and has the role 'Admin'.

        Args:
            request (Request): The current HTTP request.
            view (View): The DRF view being accessed.

        Returns:
            bool: True if user is authenticated and has role 'Admin', False otherwise.
        """


        return request.user.is_authenticated and request.user.role.role_name == 'Admin'


class VacationListApiView(generics.ListCreateAPIView):
    """
    API view to list all vacations (publicly) and allow authenticated users to create new vacations.

    - GET: Returns a list of all vacations, ordered by start date.
    - POST: Allows only authenticated users to create a new vacation.
    """
    queryset : Type[Vacation]= Vacation.objects.all().order_by('start_date')
    serializer_class = VacationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

   

class VacationUpdateApiView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific vacation.

    Access is restricted to authenticated admin users only (via IsAdminUserCustom).

    - GET: Retrieve vacation details.
    - PUT/PATCH: Update vacation information.
    - DELETE: Remove a vacation from the system.
    
    """

    queryset: Type[Vacation] = Vacation.objects.all()
    serializer_class = VacationSerializer
    permission_classes = [IsAdminUserCustom]

class CountryListApiView(generics.ListCreateAPIView):

    """
    API view to allow only admin users to:
    - GET: View the list of countries.
    - POST: Create a new country.
    All other users (even authenticated) are denied access.
    """
    queryset: Type[Country] = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAdminUserCustom]

class LikeToggleView(APIView):
    """
    API endpoint that allows authenticated users to like a vacation.

    - POST: Like a vacation if not already liked.
      Returns 400 if the user already liked the vacation.
    """
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request:Request, pk:int, *args:Any, **kwargs:Any) -> Response:
        """
        Handle POST request to like a vacation.

        Args:
            request (Request): The incoming HTTP request.
            pk (int): Primary key of the vacation to be liked.

        Returns:
            Response: 201 if liked, 400 if already liked.

            """

        vacation = get_object_or_404(Vacation, pk=pk)
        user = request.user
        if Like.objects.filter(user=user, vacation=vacation).exists():
            return Response({'detail':'Already liked'},status=status.HTTP_400_BAD_REQUEST)
        
        Like.objects.create(user=user, vacation=vacation)
        return Response({'detail':'Liked'}, status=status.HTTP_201_CREATED)

    def delete(self, request:Request, pk:int, *args:Any, **kwargs:Any) -> Response:
        """
        Unlike a vacation (if previously liked).
        
        Returns:
            - 204 No Content if unliked successfully.
            - 404 Not Found if like does not exist.
        """

        vacation = get_object_or_404(Vacation, pk=pk)
        user = request.user
        like = Like.objects.filter(user=user, vacation=vacation).first()
        if like:
            like.delete()
            return Response({'detail':'Unliked'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail':'Like not found'}, status=status.HTTP_404_NOT_FOUND)

class UserSignUpView(APIView):
    """
    API endpoint for user registration.

    - POST: Creates a new user account.
    - On success: Automatically logs the user in and returns a 200 OK.
    - On failure: Returns validation errors with 400 Bad Request.
    """
    permission_classes = [permissions.AllowAny]
    def post(self, request:Request, *args:Any, **kwargs:Any) -> Response:
        """
        Handle user sign-up via POST request.

        Args:
            request (Request): The HTTP request with user sign-up data.

        Returns:
            Response: 200 OK on successful registration and login, or
                      400 Bad Request with serializer errors.
        """
        serializer = UserSignUpSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.backend = 'users.backends.EmailBackend'
            login(request, user)
            return Response({'detail': 'Successfully log in'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LoginAPIView(APIView):

    """
    API endpoint for user login using email and password.

    - POST: Authenticates a user and starts a session (via Django's login).
    - On success: Returns 200 OK and session is started.
    - On failure: Returns 400 Bad Request with validation errors.
    """
    permission_classes = [permissions.AllowAny]
    def post(self, request:Request, *args:Any, **kwargs:Any) -> Response:

        """
        Handle POST request to log in a user.

        Args:
            request (Request): The HTTP request with login data.

        Returns:
            Response: 200 OK if login is successful, otherwise 400 Bad Request.
        """

        serializer = LoginSerializer(data=request.data, context={'request': request})

        serializer = LoginSerializer(data=request.data,context={'request': request})    

        if serializer.is_valid():
            user = serializer.validated_data['user']
            user.backend = 'users.backends.EmailBackend'
            login(request, user)
            return Response({'detail': 'Successfully log in'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):

    """
    API endpoint to log out an authenticated user.

    This view uses session-based authentication and logs the user out
    by calling Django's built-in logout() function.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request:Request, *args:Any, **kwargs:Any) -> Response:

        """
        Handle POST request to log the user out.

        Args:
            request (Request): The current HTTP request.

        Returns:
            Response: 200 OK with a confirmation message.
        """
        
        logout(request)
        return Response({'detail': 'Successfully log out'}, status=status.HTTP_200_OK)