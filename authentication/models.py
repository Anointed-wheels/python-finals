from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

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

class BaseUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError("Password must be provided")
        user = self.model(email=self.nomalize_email(email), user_type= "ADMIN")
        user.set_password(password)
        user.save()
        return user

    def _create_user(self, firstname, lastname, email, phone, password= None, **extra_fields):
        if email is None:
            raise TypeError('Users should have an Email')
        if firstname is None:
            raise TypeError('Users should have a Firstname')
        if lastname is None:
            raise TypeError('User should have a Lastname')
        if phone is None:
            raise TypeError('User should have a Phone number')

    def create_superuser(self, email, password=None, **extra_fields):
        if password is None:
            raise TypeError('Password should not be none')
        user = user._create_user(email, password)
        user.is_superuser= True
        user.is_staff = True
        user.is_verified = True
        user.role= "ADMIN"
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email= models.EmailField(max_length=255, unique=True)
    firstname= models.CharField(max_length=100)
    lastname= models.CharField(max_length=100)
    date_of_birth= models.DateField()
    phone= models.CharField(max_length= 15, unique= True)
    gender= models.CharField(max_length=6, choices=GENDER_CHOICES )
    nationality= models.CharField(max_length=100, null= True, blank= True)
    address= models.TextField(null= True, blank= True)
    profile_picture = models.ImageField(upload_to= "profile_picture/", null=True, blank=True)
    is_verified= models.BooleanField(default= False)
    is_active= models.BooleanField(default= True)
    is_staff= models.BooleanField(default= False)
    user_type= models.CharField(choices= USER_TYPE, max_length=9, default=USER_TYPE[0][0])
    staff_role = models.CharField(max_length=20, choices=STAFF_ROLES, null=True, blank=True)
    admin_secret = models.CharField(max_length= 14, null=True, blank= True)
    created_at= models.DateTimeField(auto_now_add= True)
    updated_at= models.DateTimeField(auto_now= True)
    USERNAME_FIELD= "email"
    REQUIRED_FIELDS = ['firstname', "lastname", "phone"]

    objects = BaseUserManager

    # def __str__(self):
    #     return f"{self.firstname} - {self.phone}"

    def tokens(self):
        refresh= RefreshToken.for_user(self)
        return {
            'refesh': str(refresh),
            'access': str(refresh.access_token)
        }

    class Meta:
        db_table = "user"


