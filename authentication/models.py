from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

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
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError("Password must be provided")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('user_type', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class PendingUser(models.Model):
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
    user_type= models.CharField(choices= USER_TYPE, max_length=9, default=USER_TYPE[0][0])
    staff_role = models.CharField(max_length=20, choices=STAFF_ROLES, null=True, blank=True)
    admin_secret = models.CharField(max_length= 14, null=True, blank= True)
    password = models.CharField(max_length=128, null= True, blank= True)
    created_at= models.DateTimeField(auto_now_add= True)
    token = models.CharField(max_length=6, null=True, blank=True)
    token_created_at = models.DateTimeField(null=True, blank=True)

    def is_token_valid(self, token):
        if self.token != token:
            return False
        if not self.token_created_at:
            return False
        return timezone.now() <= self.token_created_at + timedelta(minutes=5)

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

    objects = BaseUserManager()

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
