from django.urls import path
from myadmin.views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
   path('delete-user/<str:email>/', AdminDeleteUserView.as_view()),
   path('suspend-user/<str:email>/', AdminSuspendUserView.as_view()),
   path('activate-user/<str:email>/', ActivateUserView.as_view()),
   path('approve-staff/<str:email>/', ApprovePendingStaffView.as_view()),
   path('pending-staff/', PendingStaffListView.as_view()),
]