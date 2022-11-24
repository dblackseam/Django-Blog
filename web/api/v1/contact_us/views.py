import logging

from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny

from .serializers import FeedbackSerializer

logger = logging.getLogger(__name__)


class FeedbackView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FeedbackSerializer
