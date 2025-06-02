from rest_framework import serializers
from authentication.models import CustomUser, PendingUser
from django.contrib import auth
# from utils.email import send_email
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from authentication.models import GENDER_CHOICES, USER_TYPE, STAFF_ROLES

class CreateUserSerializer(serializers.ModelSerializer):
    firstname= serializers.CharField(max_length= 255)
    lastname= serializers.CharField(max_length= 255)
    email= serializers.EmailField()
    password= serializers.CharField(min_length= 8, max_length= 68, write_only= True)
    gender= serializers.ChoiceField(choices=GENDER_CHOICES)
    phone= serializers.CharField()
    address= serializers.CharField()
    nationality= serializers.CharField(required= False)
    date_of_birth= serializers.DateField()
    profile_picture= serializers.ImageField(required= False)
    user_type= serializers.ChoiceField(choices=USER_TYPE)
    staff_role= serializers.ChoiceField(choices=STAFF_ROLES, required= False, allow_blank=True, allow_null=True)
    admin_secret = serializers.CharField(max_length= 14, required= False, allow_blank=True, allow_null=True)


    def create(self, validated_data):
        raw_password = validated_data.pop("password")
        hashed_password = make_password(raw_password)
        validated_data["password"] = hashed_password
        return PendingUser.objects.create(**validated_data)


    class Meta:
        model = PendingUser
        fields = ['firstname', 'lastname', 'email', 'password', 'gender', 'phone', 'address', 'nationality', 'date_of_birth', 'profile_picture', 'user_type', "staff_role", "admin_secret"]

class ConfirmEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()

    def validate(self, attrs):
        user_type = attrs.get('user_type')
        staff_role = attrs.get('staff_role')
        admin_secret = attrs.get('admin_secret')

        if user_type == 'ADMIN' and not admin_secret:
            raise serializers.ValidationError({'admin_secret': "This field is required for staff admin"})
        if user_type != 'ADMIN' and admin_secret:
            raise serializers.ValidationError({'admin_secret': "This field is only for staff admin, kindly change staff type"})
        if user_type == "ADMIN" and admin_secret != "1234567890abcd":
            raise serializers.ValidationError({"admin_secret": 'Invalid admin key'})
        if user_type == 'STAFF' and not staff_role:
            raise serializers.ValidationError({"staff_role": "This field is required for staff users."})

        if user_type != 'STAFF' and staff_role:
            raise serializers.ValidationError({"staff_role": "Only staff users can have a staff role."})

        return attrs

    def validate(self, attrs):
        email = attrs.get("email")
        token = attrs.get("token")

        try:
            pending_user = PendingUser.objects.get(email=email)
        except PendingUser.DoesNotExist:
            raise serializers.ValidationError("This email is not registered. Please sign up.")

        if not pending_user.is_token_valid(token):
            raise serializers.ValidationError("Invalid or expired token.")

        user_type = pending_user.user_type
        staff_role = pending_user.staff_role
        admin_secret = pending_user.admin_secret

        if user_type == 'ADMIN' and not admin_secret:
            raise serializers.ValidationError({'admin_secret': "This field is required for staff admin"})
        if user_type != 'ADMIN' and admin_secret:
            raise serializers.ValidationError({'admin_secret': "This field is only for staff admin, kindly change staff type"})
        if user_type == "ADMIN" and admin_secret != "1234567890abcd":
            raise serializers.ValidationError({"admin_secret": 'Invalid admin key'})
        if user_type == 'STAFF' and not staff_role:
            raise serializers.ValidationError({"staff_role": "This field is required for staff users."})
        if user_type != 'STAFF' and staff_role:
            raise serializers.ValidationError({"staff_role": "Only staff users can have a staff role."})

        attrs["pending_user"] = pending_user
        return attrs


    def create(self, validated_data):
        pending_user = validated_data["pending_user"]

        user = CustomUser.objects.create(
            email=pending_user.email,
            firstname=pending_user.firstname,
            lastname=pending_user.lastname,
            date_of_birth=pending_user.date_of_birth,
            phone=pending_user.phone,
            gender=pending_user.gender,
            nationality=pending_user.nationality,
            address=pending_user.address,
            profile_picture=pending_user.profile_picture,
            user_type=pending_user.user_type,
            staff_role=pending_user.staff_role,
            admin_secret=pending_user.admin_secret,
            is_verified=True,
        )
        user.password = pending_user.password
        user.save()
         
        pending_user.delete()
        return user

# class SignupSerializer(serializers.ModelSerializer):
#     firstname= serializers.CharField(max_length= 255)
#     lastname= serializers.CharField(max_length= 255)
#     email= serializers.EmailField()
#     password= serializers.CharField(min_length= 8, max_length= 68, write_only= True)
#     gender= serializers.ChoiceField(choices=["MALE", "FEMALE"])
#     phone= serializers.CharField()
#     address= serializers.CharField()
#     nationality= serializers.CharField(required= False)
#     date_of_birth= serializers.DateField()
#     profile_picture= serializers.ImageField(required= False)
#     user_type= serializers.ChoiceField(choices=["CUSTOMER" ,"STAFF", "ADMIN", "OPERATORS"])
#     staff_role= serializers.ChoiceField(choices=["DRIVER", 'RIDER'], required= False, allow_blank=True, allow_null=True)
#     admin_secret = serializers.CharField(max_length= 14, required= False, allow_blank=True, allow_null=True)

#     def validate(self, attrs):
#         user_type = attrs.get('user_type')
#         staff_role = attrs.get('staff_role')
#         admin_secret = attrs.get('admin_secret')

#         if user_type == 'ADMIN' and not admin_secret:
#             raise serializers.ValidationError({'admin_secret': "This field is required for staff admin"})
#         if user_type != 'ADMIN' and admin_secret:
#             raise serializers.ValidationError({'admin_secret': "This field is only for staff admin, kindly change staff type"})
#         if user_type == "ADMIN" and admin_secret != "1234567890abcd":
#             raise serializers.ValidationError({"admin_secret": 'Invalid admin key'})
#         if user_type == 'STAFF' and not staff_role:
#             raise serializers.ValidationError({"staff_role": "This field is required for staff users."})

#         if user_type != 'STAFF' and staff_role:
#             raise serializers.ValidationError({"staff_role": "Only staff users can have a staff role."})

#         return attrs

#     class Meta:
#         model = CustomUser
#         fields = ['firstname', 'lastname', 'email', 'password', 'gender', 'phone', 'address', 'nationality', 'date_of_birth', 'profile_picture', 'user_type', "staff_role", "admin_secret"]

    


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=68, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email').lower()
        password = attrs.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('Invalid login credentials')

        if not user.check_password(password):
            raise AuthenticationFailed('Invalid login credentials')

        if not user.is_active:
            raise AuthenticationFailed('Your account has been suspended!')

        return {
            'id': user.id,
            'email': user.email,
            'tokens': user.tokens(),
        }

        
class UserUpdateSerializer(serializers.ModelSerializer):
    firstname= serializers.CharField(source= "user.firstname")
    lastname= serializers.CharField(source="user.lastname", max_length= 255)
    email= serializers.EmailField(source="user.email")
    gender= serializers.ChoiceField(source="user.gender", choices=["MALE", "FEMALE"])
    phone= serializers.CharField(source="user.phone")
    address= serializers.CharField(source="user.address")
    nationality= serializers.CharField(source="user.nationality", required= False)
    date_of_birth= serializers.DateField(source="user.date_of_birth")
    profile_picture= serializers.ImageField(source="user.profile_picture", required= False)
    user_type= serializers.ChoiceField(source="user.user_type",choices=["CUSTOMER" ,"STAFF", "ADMIN", "OPERATORS"])
    staff_role= serializers.ChoiceField(source="user.staff_role",choices=["DRIVER", 'RIDER'], required= False, allow_blank=True, allow_null=True)
    class Meta:
        model = CustomUser
        fields = ['firstname', 'lastname', 'email','gender', 'phone', 'address', 'nationality', 'date_of_birth', 'profile_picture', 'user_type', "staff_role"]

User = get_user_model()
class ChangePasswordSerializer(serializers.Serializer):
    confirm_former_password= serializers.CharField(min_length= 8, max_length= 68, write_only= True)
    new_password= serializers.CharField(min_length= 8, max_length= 68, write_only= True)


    def validate(self, attrs):
        user = self.context['request'].user
        old_password = attrs.get('confirm_former_password')

        if not user.check_password(old_password):
            raise AuthenticationFailed("Invalid current password")

        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user
