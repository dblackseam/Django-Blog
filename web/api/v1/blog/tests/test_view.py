import pytest
from django.urls import reverse
from rest_framework.test import APITestCase


@pytest.mark.skip
class ViewTest(APITestCase):
    def test_get(self):
        url = reverse("api:v1:blog:article-list")
        print(url)
        response = self.client.get(url)
        print(response)
