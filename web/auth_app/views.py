import logging

from dj_rest_auth import views as auth_views
from django.contrib.auth import logout as django_logout
from rest_framework.generics import CreateAPIView, GenericAPIView
from django.views.generic import TemplateView
from rest_framework.permissions import AllowAny
from main.tasks import send_information_email

from . import serializers
from .services import full_logout

logger = logging.getLogger(__name__)


class LoginView(auth_views.LoginView):
    serializer_class = serializers.LoginSerializer


class SignUpView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserSignUpSerializer

    def post(self, request, **kwargs):
        serializer_instance = self.get_serializer(data=request.data)
        serializer_instance.is_valid()
        serializer_instance.save()


class PasswordResetView(auth_views.PasswordResetView):
    serializer_class = serializers.PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)


class LogoutView(auth_views.LogoutView):
    allowed_methods = ('POST', 'OPTIONS')

    def session_logout(self):
        django_logout(self.request)

    def logout(self, request):
        self.session_logout()
        response = full_logout(request)
        return response
