from django.shortcuts import render
from rest_framework import views, status, generics, permissions
from rest_framework.response import Response
from authentication.serializers import SignupSerializer, LoginSerializer, UserUpdateSerializer, ChangePasswordSerializer
from authentication.models import CustomUser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class SignupView(generics.GenericAPIView):
    serializer_class= SignupSerializer
    def post(self, request):
        Serializer = self.serializer_class(data=request.data)
        Serializer.is_valid(raise_exception=True)
        

        email= Serializer.validated_data.get("email")
        phone= Serializer.validated_data.get("phone")
        password= Serializer.validated_data.get("password").lower()
        email_exist= CustomUser.objects.filter(email= email).first()

        if email_exist:
            return Response(data= {"message": "Email already exists"}, status= 400) 

        phone_exist= CustomUser.objects.filter(phone= phone).first()

        if phone_exist:
            return Response(data= {"message": "phone already exists"}, status= 400)
        user= Serializer.save()
        user.set_password(password)
        user.save()
       

        Serializer.save(email= email)
        return Response(data= Serializer.data, status= 201)

class LoginView(generics.GenericAPIView):
    serializer_class= LoginSerializer
    def post(self, request):
        Serializer = self.serializer_class(data= request.data)
        Serializer.is_valid(raise_exception=True)

        return Response(data= Serializer.data, status= 201)

class DeleteView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"detail": "User account deleted."}, status=status.HTTP_204_NO_CONTENT)

class UpdateUserProfileView(generics.GenericAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        user = request.user
        serializer = self.serializer_class(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Profile updated successfully.", "user": serializer.data}, status=status.HTTP_200_OK)


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
