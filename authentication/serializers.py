from rest_framework import serializers
from authentication.models import CustomUser
from django.contrib import auth
# from utils.email import send_email
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

class SignupSerializer(serializers.ModelSerializer):
    firstname= serializers.CharField(max_length= 255)
    lastname= serializers.CharField(max_length= 255)
    email= serializers.EmailField()
    password= serializers.CharField(min_length= 8, max_length= 68, write_only= True)
    gender= serializers.ChoiceField(choices=["MALE", "FEMALE"])
    phone= serializers.CharField()
    address= serializers.CharField()
    nationality= serializers.CharField(required= False)
    date_of_birth= serializers.DateField()
    profile_picture= serializers.ImageField(required= False)
    user_type= serializers.ChoiceField(choices=["CUSTOMER" ,"STAFF", "ADMIN", "OPERATORS"])
    staff_role= serializers.ChoiceField(choices=["DRIVER", 'RIDER'], required= False, allow_blank=True, allow_null=True)
    admin_secret = serializers.CharField(max_length= 14, required= False, allow_blank=True, allow_null=True)

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

    class Meta:
        model = CustomUser
        fields = ['firstname', 'lastname', 'email', 'password', 'gender', 'phone', 'address', 'nationality', 'date_of_birth', 'profile_picture', 'user_type', "staff_role", "admin_secret"]

    


class LoginSerializer(serializers.ModelSerializer):
    email= serializers.EmailField()
    password= serializers.CharField(min_length= 8, max_length= 68, write_only= True)
    is_active= serializers.BooleanField(source="user.is_active", read_only=True)

    class Meta:
        model = CustomUser
        fields= ['id', 'email', 'password', 'tokens', "is_active"]
    def validate(self, attrs):
        email= attrs.get('email').lower()
        password= attrs.get('password')
        is_active= attrs.get("is_active")
        user= CustomUser.objects.filter(email= email, password= password).first()

        if not user:
            raise AuthenticationFailed('invalid login credentials')
            #send email

        if is_active== False:
            raise AuthenticationFailed("Your account has been suspended!")
        data = {
            'to': user.email,
            'subject': "LOGIN NOTIFICATIONT",
            "body": "A new login was detected, if it is not you contact admin"
        }
        return {
            'id': user.id,
            'email': user.email,
            'tokens': user.tokens
        }


        # fields = ['pickoff_location', 'dropoff_location','pickup_time', 'number_of_passangers',
        #  'ride_type', 'ride_status', 'number_of_rides', 'special_request', 'payment_method'
        # ]

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
