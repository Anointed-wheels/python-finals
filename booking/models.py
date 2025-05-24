from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from authentication.models import *

# Create your models here.
GENDER_CHOICES=[
    ("MALE" , "male"),
    ("FEMALE", "female")
]
USER_TYPE=[
    ("CUSTOMER" , "customer"),
    ("STAFF" , "staff"),
    ("ADMIN", "admin"),
    ("OPERATORS", "operators"),
]
STAFF_ROLES = [
    ('DRIVER', 'driver'),
    ('RIDER', 'rider'),
]
RIDE_STATUS = [
    ('PENDING', 'pending'),
    ('ACCEPTED', 'accepted'),
    ('IN_PROGRESS', 'in_Progress'),
    ('COMPLETED', 'completed'),
    ('CANCELLED', 'cancelled'),
]
RIDE_TYPE= [
    ('BIKE', 'bike'),
    ('CAR', 'car'),
    ('BUS', 'bus'),
    ('VAN', 'van'),
]
SPECIAL_REQUEST= [
    ('YES', 'yes'),
    ("NO", "no"),
]

User = get_user_model()

class BookingModel(models.Model):
    id = models.UUIDField(primary_key= True, default= uuid. uuid4, editable= False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null= True, blank= True)
    pickoff_location = models.CharField(max_length= 255)
    dropoff_location = models.CharField(max_length= 255)
    pickup_time= models.DateTimeField()
    number_of_passangers= models.IntegerField(default=1)
    ride_type= models.CharField(choices= RIDE_TYPE, max_length= 4, default= "bike")
    ride_status= models.CharField(choices= RIDE_STATUS, max_length= 11)
    number_of_rides= models.IntegerField(default= 1)
    special_request= models.CharField(choices= SPECIAL_REQUEST, max_length= 3, default= "no", null= True, blank= True)
    payment_method= models.CharField(max_length= 50)
    created_at= models.DateTimeField(auto_now_add= True)
    updated_at= models.DateTimeField(auto_now= True)

    REQUIRED_FIELDS = [
        'pickoff_location', "dropoff_location", "pickup_time", "number_of_passangers", "ride_type", "number_of_rides", "payment_method"
    ]
    def __str__(self):
        return f'{self.name} by {self.owner.firstname} {self.owner.lastname}'
