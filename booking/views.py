from django.shortcuts import render
from booking.serializers import BookingSerializer 
from rest_framework import views, status, generics, permissions
from rest_framework.response import Response
from authentication.models import CustomUser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from booking.permissions import IsCustomerUser
from booking.models import BookingModel

# Create your views here.
class BookingView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsCustomerUser]
    serializer_class= BookingSerializer
    def post(self, request):
        Serializer = self.serializer_class(data= request.data)
        Serializer.is_valid(raise_exception=True)
        Serializer.save(user=request.user)
        return Response(data= Serializer.data, status=status.HTTP_201_CREATED)


class DeleteBookingView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = BookingModel.objects.all()

    def delete(self, request, pk):
        try:
            ride_request = BookingModel.objects.get(pk=pk, user=request.user)
            ride_request.delete()
            return Response({"detail": "Ride request deleted."}, status=status.HTTP_204_NO_CONTENT)
        except BookingModel.DoesNotExist:
            return Response({"detail": "Ride request not found."}, status=status.HTTP_404_NOT_FOUND)