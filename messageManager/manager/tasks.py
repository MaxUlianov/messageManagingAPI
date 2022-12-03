from .serializers import MessageSerializer, ClientSerializer, MailingSerializer
from .models import Message, Client, Mailing
from celery import shared_task
import requests
from messageManager.settings import TOKEN


def message_request():
    token = TOKEN
    msgid = 1

    url = f'https://probe.fbrq.cloud/v1/send/{msgid}'

    data = {
        "id": msgid,
        "phone": 0,
        "text": "string"
    }

    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    res = requests.post(url, headers=headers, json=data)
    # res_m = res.json()['message']


@shared_task()
def send_message(mail_id):
    mailing = Mailing.objects.filter(id=mail_id)
    client_filter_tag = mailing.filter_tag
    client_filter_code = mailing.filter_mobile_code

    if client_filter_tag != '':
        client_list = Client.object.filter(tag=client_filter_tag)
    elif client_filter_code != '':
        client_list = Client.object.filter(mobile_code=client_filter_code)
    else:
        client_list = Client.objects.all()

    for client in client_list:
        print(client)
        pass

    # for clients
    # make request
    # whatever data comes, save as message object
    # next one

    url = 'https://probe.fbrq.cloud/docs'
