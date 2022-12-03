# from .serializers import MessageSerializer, ClientSerializer, MailingSerializer
from .models import Message, Client, Mailing
from celery import shared_task
import requests
from datetime import datetime
from django.db import transaction, IntegrityError
from messageManager.settings import TOKEN
import logging

logger = logging.getLogger(__name__)
"""
Message sending, done as Celery task
"""


def message_request(msgid: int, phone: str, text: str):
    """
    Helper function, makes a request (sends message) to API;

    TOKEN loads from environment variable

    :param msgid: message id
    :param phone: target client's phone number
    :param text: message text
    :return: API response to request (Response object)
    """
    token = TOKEN

    url = f'https://probe.fbrq.cloud/v1/send/{msgid}'

    data = {
        "id": msgid,
        "phone": phone,
        "text": text
    }

    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    res = requests.post(url, headers=headers, json=data)
    return res


@shared_task()
def send_message(mail_id: int):
    """
    Celery task function, creates new message and sends to all clients, to who
    mailing filter applies
    :param mail_id: mailing id
    :return: 'Completed'
    """
    mailing = Mailing.objects.filter(id=mail_id)[0]
    client_filter_tag = mailing.filter_tag
    client_filter_code = mailing.filter_mobile_code

    if client_filter_tag != '':
        client_list = Client.objects.filter(tag=client_filter_tag)
    elif client_filter_code != '':
        client_list = Client.objects.filter(mobile_code=client_filter_code)
    else:
        client_list = Client.objects.all()

    for client in client_list:
        try:
            with transaction.atomic():
                new_message = Message(id_mailing=mailing, id_client=client, send_time=datetime.now())
                new_message.save()

                resp = message_request(new_message.id, client.phone, mailing.text)
                logger.info(f'Message id: {new_message.id} Request: {resp.request.url, resp.request.headers, resp.request.body}')
                logger.info(f'Response = {resp}\n')

                if resp.status_code == 200:
                    if resp.json()['message'] == 'OK':
                        status = True
                else:
                    status = False

                new_message.status = status
                new_message.save()
        except IntegrityError:
            logger.warning(f'Error: {repr(IntegrityError)}')
    return 'Completed'
