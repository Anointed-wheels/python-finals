from django.shortcuts import render
# from admin.serializers import AdminSerializer
from rest_framework import views, status, generics
from rest_framework.response import Response
from authentication.models import CustomUser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
# from admin.models import AdminModel
from myadmin.permissions import IsAdminUser
from django.contrib.auth import get_user_model

# Create your views here.
User = get_user_model()
class AdminDeleteUserView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = User.objects.all()

    def delete(self, request, email):
        try:
            user = User.objects.get(email__iexact=email)
            user.delete()
            return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class AdminSuspendUserView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]

    def post(self, request, email):
        try:
            user = User.objects.get(email__iexact=email)
            user.is_active = False
            user.save()
            return Response({"detail": "User suspended successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class ActivateUserView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]

    def post(self, request, email):
        try:
            user = User.objects.get(email__iexact=email)
            user.is_active = True
            user.save()
            return Response({"detail": "User is now active."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)