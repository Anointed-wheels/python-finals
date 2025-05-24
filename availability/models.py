from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from authentication.models import *

# Create your models here.
class AvailabilityModel(models.Model):
    titled_name = models.CharField(max_length= 259, null= True, blank= True)
    id = models.UUIDField(primary_key= True, default= uuid. uuid4, editable= False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null= True, blank= True)
    is_available= models.BooleanField(default= False)
    current_location= models.CharField(max_length= 255)
    signin_time= models.DateTimeField(auto_now= True)

    REQUIRED_FIELDS = [
        "is_available", "current_location",
    ]
    def __str__(self):
        return f'{self.name} by {self.owner.firstname} {self.owner.lastname}'