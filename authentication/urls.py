from django.urls import path, include
from .views import SignUpView, LoginView, UserDetailView, PasswordResetRequestView, ResetPasswordView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserDetailView.as_view(), name='user_detail'),
    path('forgot-password/', PasswordResetRequestView.as_view(), name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', ResetPasswordView.as_view(), name='reset_password'),

    # Allauth Urls (Google and Twitter)
    path('accounts/', include('allauth.urls')),
]