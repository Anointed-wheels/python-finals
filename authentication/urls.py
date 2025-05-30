from django.urls import path
from authentication.views import CreateUserView, ConfirmEmailView, LoginView, DeleteView, UpdateUserProfileView,ChangePasswordView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
   path('signup/', CreateUserView.as_view()),
   path('confirm-email/', ConfirmEmailView.as_view()),
   path('login/', LoginView.as_view()),
   path('delete-user/', DeleteView.as_view()),
   path('user/update/', UpdateUserProfileView.as_view()),
   path('change-password/', ChangePasswordView.as_view()),
   path('refresh-token/', TokenRefreshView.as_view(), name= 'token-refresh')
]