from django.urls import path
from booking.views import BookingView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
   path('booking/', BookingView.as_view()),
]