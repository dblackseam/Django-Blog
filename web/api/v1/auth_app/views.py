from dj_rest_auth import views as auth_views
from django.contrib.auth import logout as django_logout
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from main.models import User
from rest_framework.exceptions import ValidationError

from . import serializers
from .services import AuthAppService, full_logout, ResetPassword


class SignUpView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserSignUpSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = AuthAppService()
        service.create_user(serializer.validated_data)
        return Response(
            {'detail': _('Confirmation email has been sent')},
            status=status.HTTP_201_CREATED,
        )


class LoginView(auth_views.LoginView):
    serializer_class = serializers.LoginSerializer


class LogoutView(auth_views.LogoutView):
    allowed_methods = ('POST', 'OPTIONS')

    def session_logout(self):
        django_logout(self.request)

    def logout(self, request):
        response = full_logout(request)
        return response


class PasswordResetView(GenericAPIView):  # эта вьюшка отвечает за отправку письма
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        found_user = User.objects.filter(email=serializer.validated_data['email'])
        if not found_user:
            raise ValidationError({"key": "The user doesn't exist."})

        service = ResetPassword(found_user[0])
        service.send_email()

        return Response(
            {'detail': _('Password reset e-mail has been sent.')},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = serializers.PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = AuthAppService()
        key = serializer.validated_data["key"]
        uid = serializer.validated_data["uid"]
        if service.validate_user(key) and service.compare_userid_and_key(key, uid):
            service.change_password(uid, serializer.validated_data["password_1"])
            return Response(
                {'detail': _('Password has been reset with the new password.')},
                status=status.HTTP_200_OK,
            )


class VerifyEmailView(GenericAPIView):
    serializer_class = serializers.VerifyEmailSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)  # request.data это request.POST и request.FILES в одном
        serializer.is_valid(raise_exception=True)
        service = AuthAppService()

        if service.validate_user(request.data["key"]):  # request.data возвращает словарь
            return Response(
                {'detail': _('Ok')},
                status=status.HTTP_200_OK,
            )
