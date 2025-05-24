from rest_framework import serializers
from authentication.models import CustomUser
from booking.models import BookingModel
from django.contrib import auth
# from utils.email import send_email
from rest_framework.exceptions import AuthenticationFailed



class BookingSerializer(serializers.ModelSerializer):
    pickoff_location = serializers.CharField(max_length= 255)
    dropoff_location = serializers.CharField(max_length= 255)
    pickup_time= serializers.DateTimeField(required= False, allow_null=True)
    number_of_passangers= serializers.IntegerField(max_value= 33, default=1)
    ride_type= serializers.ChoiceField(choices=["BIKE" ,"CAR", "BUS", "VAN"])
    ride_status= serializers.ChoiceField(choices=['PENDING', 'ACCEPTED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED'])
    number_of_rides= serializers.IntegerField(default= 1)
    special_request= serializers.ChoiceField(choices=["YES", "NO"], default= "NO")
    payment_method= serializers.CharField(max_length= 255)

    def validate(self, attrs):
        ride_type = attrs.get('ride_type')
        number_of_rides = attrs.get('number_of_rides')
        number_of_passangers = attrs.get('number_of_passangers')
        special_request= attrs.get("special_request")


        if ride_type == 'BIKE':
            max_passengers = number_of_rides * 2
            if number_of_passangers > max_passengers:
                raise serializers.ValidationError({
                    'number_of_passangers': f"Maximum {max_passengers} passengers allowed for {number_of_rides} bike ride(s)."
                })


        # if ride_type == 'BIKE' and number_of_passangers > 2 and number_of_rides == 1:
        #     raise serializers.ValidationError({'number_of_passanger': "The maximum number of passanger for a bike is 2"})
        # if ride_type == 'BIKE' and number_of_rides == 2 and number_of_passangers > 4 :
        #     raise serializers.ValidationError({'number_of_passanger': "The maximum number of passanger for a bike is 2 you will have to book for more rides"})
        # if ride_type == 'BIKE' and number_of_rides == 3 and number_of_passangers > 6:
        #     raise serializers.ValidationError({'number_of_passanger': "The maximum number of passanger for a bike is 2 you will have to book for other ride types which include CAR and BUS"})
        if special_request!="YES" and number_of_rides > 3:
            raise serializers.ValidationError({'number_of_rides': "The maximum number of rides you can request at a time is 3"})
        return attrs

    class Meta:
        model= BookingModel
        exclude = ['user']