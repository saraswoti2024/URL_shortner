from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *

urlpatterns = [
    path('login/', CustomToken.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register_email/',EmailRegister.as_view(),name="email_register"),
    path('verify-email/',EmailVerify.as_view(),name="email_verification"),
    path('resend-emailverify/',ResendEmailVerification.as_view(),name="email_verification"),
    path('logout/',LogoutView.as_view(),name="logout"),
]