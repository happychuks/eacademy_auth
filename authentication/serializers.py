from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.conf import settings

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model
    """
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True},
            'password2': {'write_only': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Validate password
        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['email']  # Set username to email for compatibility
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """"
    Serializer for JWT authentication
    """
    username_field = 'email'

class PasswordResetRequestSerializer(serializers.Serializer):
    """"
    Serializer for password reset request
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = f"{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}/"

        context = {
            'user': user,
            'reset_url': reset_url,
        }

        subject = 'Password Reset Request'
        message = render_to_string('password_reset_email.html', context)
        send_mail(subject, message=message, html_message=message, from_email=None, recipient_list=[user.email])

class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for password reset
    """
    uid = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            uid = urlsafe_base64_decode(attrs['uid']).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError('Invalid user')

        if not default_token_generator.check_token(user, attrs['token']):
            raise serializers.ValidationError('Invalid token')
        
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Password fields didn't match.")

        # Validate password
        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return attrs

    def save(self):
        uid = self.validated_data['uid']
        user = User.objects.get(pk=urlsafe_base64_decode(uid).decode())
        user.set_password(self.validated_data['password'])
        user.save()