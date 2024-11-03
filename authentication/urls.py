from django.urls import path
from .views import SignUpView, LoginView, UserDetailView, ForgotPasswordView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserDetailView.as_view(), name='user_detail'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
]