from rest_framework import generics, status, views
from rest_framework.response import Response
from .models import User
from .serializers import RegisterSerializer, LoginSerializer
from .utils import send_verification_email, password_reset_confirm
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()

# Register View
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        send_verification_email(self.request, user)

# Login View
class LoginView(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

# Email Verification View
class VerifyEmailView(views.APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({'error': 'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Email verified successfully'})
        return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

# Password Reset Request
class PasswordResetRequestView(views.APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            password_reset_confirm(request, user)
            return Response({'message': 'Password reset email sent'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

# Password Reset Confirm
class PasswordResetConfirmView(views.APIView):
    def post(self, request, uidb64, token):
        new_password = request.data.get('new_password')
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({'error': 'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password reset successful'})
        return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
