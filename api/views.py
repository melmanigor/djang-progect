from django.shortcuts import render
from rest_framework import generics,permissions,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from vacation.models import Vacation,Country,Like
from .serializers import VacationSerializer,CountrySerializer,LikeSerializer


class VacationListApiView(generics.ListCreateAPIView):
    queryset = Vacation.objects.all().order_by('start_date')
    serializer_class = VacationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

   

class VacationUpdateApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vacation.objects.all()
    serializer_class = VacationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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