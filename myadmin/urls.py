from django.urls import path
from myadmin.views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
   path('delete-user/<str:email>/', AdminDeleteUserView.as_view()),
]