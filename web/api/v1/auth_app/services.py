from abc import ABC
from datetime import date, timedelta
from typing import TYPE_CHECKING, Literal, NamedTuple, Optional

from typing import TYPE_CHECKING, NamedTuple
from urllib.parse import urlencode, urljoin

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import signing
from django.core.signing import BadSignature
from django.db import transaction
from django.utils.translation import gettext_lazy as _, get_language
from rest_framework import status
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from contact_us.models import Feedback
from api.email_services import BaseEmailHandler
from main.decorators import except_shell

if TYPE_CHECKING:
    from main.models import UserType

User: 'UserType' = get_user_model()


class CreateUserData(NamedTuple):
    first_name: str
    last_name: str
    email: str
    password_1: str
    password_2: str


class AccountServicesEmailHandler(BaseEmailHandler):
    FRONTEND_URL = settings.FRONTEND_URL
    TEMPLATE_NAME = ''

    def __init__(self, user: Optional[User] = None, language: str = 'en'):
        super().__init__(user, language)


class Confirmation(AccountServicesEmailHandler):
    FRONTEND_PATH = '/confirm/'
    TEMPLATE_NAME = 'emails/verify_email.html'

    def _get_activate_url(self) -> str:
        url = urljoin(self.FRONTEND_URL, self.FRONTEND_PATH)
        query_params: str = urlencode(
            {
                'key': self.user.confirmation_key,
            },
            safe=':+',
        )
        return f'{url}?{query_params}'

    def email_kwargs(self, **kwargs) -> dict:
        return {
            'subject': _('Register confirmation email'),
            'to_email': self.user.email,
            'context': {
                'user': self.user.get_full_name(),
                'activate_url': self._get_activate_url(),
            },
        }


class ResetPassword(AccountServicesEmailHandler):
    FRONTEND_PATH = "/password-recovery/"
    TEMPLATE_NAME = "emails/reset_password_email.html"

    def _get_reset_password_url(self) -> str:
        url = urljoin(self.FRONTEND_URL, self.FRONTEND_PATH)
        query_params: str = urlencode(
            {
                "key": self.user.confirmation_key,
                "uid": self.user.id
            },
            safe=":+",
        )
        return f'{url}?{query_params}'

    def email_kwargs(self, **kwargs) -> dict:
        return {
            'subject': _('Reset your password'),
            'to_email': self.user.email,
            'context': {
                'user': self.user.get_full_name(),
                'reset_password_url': self._get_reset_password_url(),
            }
        }


class AuthAppService:
    @staticmethod
    def is_user_exist(email: str) -> bool:
        return User.objects.filter(email=email).exists()

    @staticmethod
    @except_shell((User.DoesNotExist,))
    def get_user(email: str) -> User:
        return User.objects.get(email=email)

    @transaction.atomic()
    def create_user(self, validated_data: dict):
        data = CreateUserData(**validated_data)
        print(f'{data=}')
        user = User.objects.create_user(
            email=data.email,
            first_name=data.first_name,
            last_name=data.last_name,
            password=data.password_2
        )
        confirmation_instance = Confirmation(user=user)
        print(f"{user=}")
        confirmation_instance.send_email()
        return User

    @staticmethod
    def validate_user(key: str):
        found_user = User.from_key(key)
        if found_user is None:
            raise ValidationError({"key": "Something went wrong with the key. Please, try again or contact the "
                                          "administration."})
        elif found_user.is_active:
            raise ValidationError({"key": "Your account is already activated."})
        else:
            found_user.is_active = True
            found_user.save(update_fields=["is_active"])
        return True

    @staticmethod
    def compare_userid_and_key(key, uid):
        user = User.from_key(key)
        if user.id == uid:
            return True
        else:
            raise ValidationError({"key": "Key and Userid doesn't match each other, please try again or contact the "
                                          "administration."})

    @staticmethod
    def change_password(uid, new_password):
        user = User.objects.get(uid)
        user.objects.set_password(new_password)
        user.save(update_fields=["password"])


def full_logout(request):
    response = Response({"detail": _("Successfully logged out.")}, status=status.HTTP_200_OK)
    if cookie_name := getattr(settings, 'JWT_AUTH_COOKIE', None):
        response.delete_cookie(cookie_name)
    refresh_cookie_name = getattr(settings, 'JWT_AUTH_REFRESH_COOKIE', None)
    refresh_token = request.COOKIES.get(refresh_cookie_name)
    if refresh_cookie_name:
        response.delete_cookie(refresh_cookie_name)
    if 'rest_framework_simplejwt.token_blacklist' in settings.INSTALLED_APPS:
        # add refresh token to blacklist
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except KeyError:
            response.data = {"detail": _("Refresh token was not included in request data.")}
            response.status_code = status.HTTP_401_UNAUTHORIZED
        except (TokenError, AttributeError, TypeError) as error:
            if hasattr(error, 'args'):
                if 'Token is blacklisted' in error.args or 'Token is invalid or expired' in error.args:
                    response.data = {"detail": _(error.args[0])}
                    response.status_code = status.HTTP_401_UNAUTHORIZED
                else:
                    response.data = {"detail": _("An error has occurred.")}
                    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            else:
                response.data = {"detail": _("An error has occurred.")}
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    else:
        message = _(
            "Neither cookies or blacklist are enabled, so the token "
            "has not been deleted server side. Please make sure the token is deleted client side."
        )
        response.data = {"detail": message}
        response.status_code = status.HTTP_200_OK
    return response
