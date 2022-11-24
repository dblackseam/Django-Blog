from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

from django.contrib.auth import get_user_model
from django.utils.translation import get_language

from main.tasks import send_information_email
# from __future__ import annotations

if TYPE_CHECKING:
    from main.models import UserType


User: 'UserType' = get_user_model()


class BaseEmailHandler(ABC):

    TEMPLATE_NAME: str = NotImplemented

    def __init__(self, user: Optional[User] = None, language: Optional[str] = None):
        self.user = user
        self._locale: str = language or get_language()

    @property
    def locale(self) -> str:
        return self._locale

    def send_email(self):
        kwargs = self.email_kwargs()  # Я думаю что этот момент задумывался с целью получения актуального атрибута
        # класса который и содержит все заданные кварги, т.к. тут не получить сам kwargs атрибут, потому что он задан
        # в дочернем классе.  #ТУТ НАПИСАЛ ЕРУНДУ, Т.К. SEND_EMAIL БУДЕТ ТАКЖЕ ИСПОЛЬЗОВАТЬСЯ ЭКЗЕМПЛЯРОМ СВОЙ,
        # И СО СВОИМ EMAIL_KWARGS. ЕЩЕ РАЗ: ВЫЗОВ SELF.EMAIL_KWARGS ПРОИСХОДИТ НА УРОВНЕ ДОЧЕРНЕГО КЛАССА ТАКЖЕ КАК И
        # В ЦЕЛОМ ВЫЗОВ SEND_EMAIL.
        default_kwargs = {
            'template_name': self.TEMPLATE_NAME,
            'letter_language': self.locale,
        }
        kwargs.update(default_kwargs)
        return send_information_email.apply_async(kwargs=kwargs)

    @abstractmethod
    def email_kwargs(self, **kwargs) -> dict:
        """Provide a dict with at least subject, to_email and context keys"""
