from django.shortcuts import render
from booking.serializers import BookingSerializer 
from rest_framework import views, status, generics
from rest_framework.response import Response
from authentication.models import CustomUser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from booking.permissions import IsCustomerUser

# Create your views here.
class BookingView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsCustomerUser]
    serializer_class= BookingSerializer
    def post(self, request):
        Serializer = self.serializer_class(data= request.data)
        Serializer.is_valid(raise_exception=True)
        Serializer.save(user=request.user)
        return Response(data= Serializer.data, status=status.HTTP_201_CREATED)