from django.shortcuts import render
# from admin.serializers import AdminSerializer
from rest_framework import views, status, generics
from rest_framework.response import Response
from authentication.models import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from authentication.serializers import PendingStaffSerializer
# from admin.models import AdminModel
from myadmin.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from utils.email import send_activation


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

class ApprovePendingStaffView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]

    def post(self, request, email):
        try:
            pending_staff = PendingStaff.objects.get(email=email)
        except PendingStaff.DoesNotExist:
            return Response({"error": "Pending staff not found with that email"}, status=status.HTTP_404_NOT_FOUND)

        # Check if already exists in CustomUser
        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "User already exists in system"}, status=status.HTTP_400_BAD_REQUEST)

        # Create user in CustomUser
        user = CustomUser.objects.create(
            email=pending_staff.email,
            firstname=pending_staff.firstname,
            lastname=pending_staff.lastname,
            date_of_birth=pending_staff.date_of_birth,
            phone=pending_staff.phone,
            gender=pending_staff.gender,
            nationality=pending_staff.nationality,
            address=pending_staff.address,
            profile_picture=pending_staff.profile_picture,
            user_type=pending_staff.user_type,
            staff_role=pending_staff.staff_role,
            admin_secret=pending_staff.admin_secret,
            is_verified=True,
            is_active=True,
        )
        user.password = pending_staff.password
        user.save()

        send_activation(user.email, user.firstname)

        pending_staff.delete()

        return Response(
            {"message": f"{user.user_type} account for {user.email} approved and activated."},
            status=status.HTTP_201_CREATED
        )

class PendingStaffListView(ListAPIView):
    queryset = PendingStaff.objects.all()
    serializer_class = PendingStaffSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]