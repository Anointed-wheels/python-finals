from rest_framework import serializers
from django.utils import timezone
from authentication.models import CustomUser
from availability.models import AvailabilityModel
from django.contrib import auth
from authentication.models import CustomUser
# from utils.email import send_email
from rest_framework.exceptions import AuthenticationFailed

class AvailabilitySerializer(serializers.ModelSerializer):
    profile_picture= serializers.CharField(source='user.profile_picture', read_only= True)
    phone = serializers.CharField(source='user.phone', read_only=True)
    firstname= serializers.CharField(source='user.firstname', read_only=True)
    is_available= serializers.BooleanField(default= False)
    staff_role= serializers.CharField(source='user.staff_role', read_only=True)
    gender= serializers.CharField(source='user.gender', read_only=True)
    current_location= serializers.CharField(max_length=255)
    signin_time= serializers.DateTimeField(read_only= True)
    titled_name = serializers.SerializerMethodField()

    def get_titled_name(self, obj):
        gender = obj.user.gender.lower()
        if gender == "male":
            prefix = "Mr."
        else:
            prefix = "Mrs."
        return f"{prefix} {obj.user.firstname}"

    def create(self, validated_data):
        validated_data['signin_time'] = timezone.now()
        return super().create(validated_data)

    def validate(self, attrs):
        is_available = attrs.get('is_available')

        if is_available == False:
            raise serializers.ValidationError({'is_available': "You cannot signin with the availability of false, change to True "})
        return attrs


    class Meta:
        model = AvailabilityModel
        fields=  ['id', 'user',"titled_name", "profile_picture", 'phone', 'firstname', 'is_available', 'staff_role', 'gender', 'current_location', "signin_time"]
        read_only_fields= ['user']