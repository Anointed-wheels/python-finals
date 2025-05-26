from django.shortcuts import render
from availability.serializers import AvailabilitySerializer
from rest_framework import views, status, generics
from rest_framework.response import Response
from authentication.models import CustomUser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from availability.models import AvailabilityModel
from availability.permissions import IsStaffUser
# from booking.permissions import IsCustomerUser

# Create your views here.
class AvailabilityView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class= AvailabilitySerializer
    def post(self, request):
        Serializer = self.serializer_class(data= request.data)
        Serializer.is_valid(raise_exception=True)
        Serializer.save(user=request.user)
        return Response(data= Serializer.data, status=status.HTTP_201_CREATED)

class AvailableDriversView(generics.GenericAPIView):
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        available_drivers = AvailabilityModel.objects.filter(is_available=True)
        serializer = self.get_serializer(available_drivers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
