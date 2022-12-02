from rest_framework import serializers
from .models import Mailing, Message, Client


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
        fields = ["id", "start_time", "text", "filter", "end_time"]
