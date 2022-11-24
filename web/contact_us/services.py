from django.utils.translation import gettext_lazy as _

from contact_us.models import Feedback
from api.v1.auth_app.services import BaseEmailHandler
from src.settings import FRONTEND_URL
from urllib.parse import urljoin


class ContactUsService(BaseEmailHandler):
    FRONTEND_URL = urljoin(FRONTEND_URL, "/admin/contact_us/feedback/")

    def __init__(self, feedback: Feedback):
        self.feedback = feedback  # Добавил новый атрибут в базовый класс BaseEmailHandler!
        self.kwargs = {}
        super().__init__()  # ПРИ ЭТОМ ОСТАВИВ ОСТАЛЬНЫЕ!

    def email_kwargs(self) -> dict:
        return self.kwargs

    def send_email_notification_to_user(self):
        self.TEMPLATE_NAME = "emails/user_notification.html"

        self.kwargs = {
            "subject": _("Thank you for reaching out to us!"),
            "to_email": self.feedback.email,
            "context": {
                "user": self.feedback.name,
            }
        }  # self.kwargs были переопределены дабы не делать self.kwargs.update(), помним что проект который запущен
        # как сервер работает всегда, единожды определив kwagrs и делая каждый раз update мы просто будем обновлять
        # имеющийся словарь перезаписывая его, это может привести к неожиданным атрибутам в контексте.

        self.send_email()

    def send_information_to_admin(self):
        self.TEMPLATE_NAME = "emails/admin_notification.html"

        self.kwargs = {
            "subject": "New message from contact_us form!",
            "to_email": "admin.admin@mail.com",
            "context": {
                "user": self.feedback.name,
                "email": self.feedback.email,
                "link": urljoin(self.FRONTEND_URL, str(self.feedback.pk))
            }
        }

        self.send_email()

    def send_answer_to_user(self):
        self.TEMPLATE_NAME = "emails/user_answer.html"

        self.kwargs = {
            "subject": _("Reply to your appeal"),
            "to_email": self.feedback.email,
            "context": {
                "user": self.feedback.name,
                "answer": self.feedback.answer,
            }
        }

        self.send_email()
