import re

import pytest
from rest_framework.reverse import reverse
from django.test import override_settings
from django.core import mail

pytestmark = [pytest.mark.django_db]


@override_settings(
    CELERY_TASK_ALWAYS_EAGER=True,
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
)
def test_register_flow(client):  # client - это фикстура
    data = {
        "first_name": "string",
        "last_name": "string",
        "email": "user@example.com",
        "password_1": "stringst",
        "password_2": "stringst"
    }
    url = reverse("api:v1:auth_app:sign-up")  # reverse используется для того что бы выцепить url по имени url в
    # path, к нему также в kwargs можно передать query параметры. Эта же фунцкия используется в get_absolute_url в
    # модели, дабы генерировать ссылку по запросу внутри темплейта или в иных местах где есть доступ к модели(
    # экземплярам).
    response = client.post(url, data)

    assert response.status_code == 201
    assert len(mail.outbox) == 1
    letter = mail.outbox[0]
    assert letter.subject == "Register confirmation email"
    # print(letter.message())
    pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(pattern, str(letter.message()))
    print(urls)
    assert urls, 'wrong url pattern'


def test_passwords_check(client):
    data = {
        "first_name": "string",
        "last_name": "string",
        "email": "user@example.com",
        "password_1": "stringst",
        "password_2": "stringst1"
    }

    url = reverse("api:v1:auth_app:sign-up")
    response = client.post(url, data)

    assert response.status_code == 400
