from .serializers import MessageSerializer, ClientSerializer, MailingSerializer
from .models import Message, Client, Mailing


def send_message(mail_id):
    mailing = Mailing.objects.filter(id=mail_id)
    client_filter = mailing.filter

