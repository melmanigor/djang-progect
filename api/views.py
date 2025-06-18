from django.shortcuts import render
from rest_framework import generics,permissions,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.contrib.auth import login,logout
from vacation.models import Vacation,Country,Like
from .serializers import VacationSerializer,CountrySerializer,LikeSerializer, LoginSerializer,UserSignUpSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import BasePermission

class IsAdminUserCustom(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.role_name == 'Admin'


class VacationListApiView(generics.ListCreateAPIView):
    queryset = Vacation.objects.all().order_by('start_date')
    serializer_class = VacationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

   

class VacationUpdateApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vacation.objects.all()
    serializer_class = VacationSerializer
    permission_classes = [IsAdminUserCustom]

class CountryListApiView(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.AllowAny]

class LikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        vacation = get_object_or_404(Vacation, pk=pk)
        user = request.user
        if Like.objects.filter(user=user, vacation=vacation).exists():
            return Response({'detail':'Already liked'},status=status.HTTP_400_BAD_REQUEST)
        
        Like.objects.create(user=user, vacation=vacation)
        return Response({'detail':'Liked'}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        vacation = get_object_or_404(Vacation, pk=pk)
        user = request.user
        like = Like.objects.filter(user=user, vacation=vacation).first()
        if like:
            like.delete()
            return Response({'detail':'Unliked'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail':'Like not found'}, status=status.HTTP_404_NOT_FOUND)

class UserSignUpView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.backend = 'users.backends.EmailBackend'
            login(request, user)
            return Response({'detail': 'Successfully log in'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data,context={'request': request})    

        if serializer.is_valid():
            user = serializer.validated_data['user']
            user.backend = 'users.backends.EmailBackend'
            login(request, user)
            return Response({'detail': 'Successfully log in'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class LogoutAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        print("request.user =", request.user)
        print("authenticated =", request.user.is_authenticated)
        logout(request)
        return Response({'detail': 'Successfully log out'}, status=status.HTTP_200_OK)
@method_decorator(csrf_exempt, name='dispatch')
class MeAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "username": request.user.username,
            "session_key": request.session.session_key,
            "is_authenticated": request.user.is_authenticated
        })