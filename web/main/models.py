from typing import TypeVar, Optional

from django.contrib.auth.models import AbstractUser
from django.core import signing
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .managers import UserManager

UserType = TypeVar('UserType', bound='User')


class User(AbstractUser):
    username = None  # type: ignore
    email = models.EmailField(_('Email address'), unique=True)
    is_active = models.BooleanField(_('Is active'), default=False)

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()  # type: ignore

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self) -> str:
        return self.email

    @property
    def full_name(self) -> str:
        return super().get_full_name()

    @property
    def confirmation_key(self) -> str:
        return signing.dumps(obj=self.pk)

    @classmethod
    def from_key(cls, key: str) -> Optional[UserType]:
        max_age = 60 * 60 * 24 * settings.EMAIL_CONFIRMATION_EXPIRE_DAYS
        try:
            pk = signing.loads(key, max_age=max_age)
            user = cls.objects.get(id=pk)
        except (signing.SignatureExpired, signing.BadSignature, cls.DoesNotExist):
            user = None
        return user
