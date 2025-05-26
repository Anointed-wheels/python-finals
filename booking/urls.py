from django.urls import path
from booking.views import BookingView, DeleteBookingView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
   path('booking/', BookingView.as_view()),
   path('cancel-booking/<uuid:pk>/', DeleteBookingView.as_view())
]