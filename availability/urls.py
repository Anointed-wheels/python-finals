from django.urls import path
from availability.views import AvailabilityView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
   path('availability/', AvailabilityView.as_view()),
]