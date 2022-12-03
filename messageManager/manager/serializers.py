from rest_framework import serializers
from .models import Mailing, Message, Client

"""Serializers for API json data handling"""


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "send_time", "status", "id_mailing", "id_client"]


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "phone", "mobile_code", "tag", "timezone"]


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = ["id", "start_time", "text", "filter_mobile_code", "filter_tag", "end_time", "celery_task_id"]
