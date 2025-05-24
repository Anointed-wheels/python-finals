from django.urls import path
from authentication.views import SignupView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
   path('signup/', SignupView.as_view()),
   path('login/', LoginView.as_view()),
   path('refresh-token/', TokenRefreshView.as_view(), name= 'token-refresh')
]