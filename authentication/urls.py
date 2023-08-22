from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserDetailsView, RegisterUserView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-details/', UserDetailsView.as_view(), name='current-user-details'),
    path('register/', RegisterUserView.as_view(), name='register-user')
]
