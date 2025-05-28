from django.urls import path
from availability.views import AvailabilityView, AvailableDriversView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
   path('availability/', AvailabilityView.as_view()),
   path('see_availables/', AvailableDriversView.as_view()),
]