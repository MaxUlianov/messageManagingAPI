# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from celery import uuid
from celery import current_app

from .serializers import MessageSerializer, ClientSerializer, MailingSerializer
from .models import Message, Client, Mailing
from .tasks import send_message
import logging

logger = logging.getLogger(__name__)


def index(request):
    return


class ObjectApiView(APIView):
    def get(self, model, model_serializer, request, *args, **kwargs):
        """
        List all the objects (mailings / clients / messages)
        """
        mailings = model.objects.all()
        serializer = model_serializer(mailings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, model, model_serializer, data, request, *args, **kwargs):
        """
        Create new object (mailing, client, message) with given parameters
        """
        serializer = model_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObjectDetailsApiView(APIView):
    def get_object(self, object_id, model, *args, **kwargs):
        """
        Helper for accessing Objects
        """
        try:
            return model.objects.get(id=object_id)
        except model.DoesNotExist:
            return None

    def get(self, request, object_id, model, model_serializer, *args, **kwargs):
        """
        Get Object with given id
        """
        instance = self.get_object(object_id, model)
        if not instance:
            return Response(
                {"resp": "Object with such id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = model_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, object_id, model, model_serializer, data, task=None, *args, **kwargs):
        """
        Update Object with given id, if exists
        """
        instance = self.get_object(object_id, model)
        if not instance:
            return Response(
                {"resp": "Object with such id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = model_serializer(instance = instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, object_id, model, model_serializer, *args, **kwargs):
        """
        Delete Object with given id
        """
        instance = self.get_object(object_id, model)
        if not instance:
            return Response(
                {"resp": "Object with such id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        instance.delete()
        return Response(
            {"resp": "Object successfully deleted"},
            status=status.HTTP_200_OK
        )


class MailingApiView(ObjectApiView):
    def get(self, request, *args, **kwargs):
        """Get all mailings"""
        return ObjectApiView.get(self, Mailing, MailingSerializer, request)

    def post(self, request, *args, **kwargs):
        """
        Create new Mailing object with given parameters and schedule message sending
        with celery
        (Override of parent method)
        """
        task_id = uuid()

        data = {
            'start_time': request.data.get('start_time'),
            'text': request.data.get('text'),
            'filter_mobile_code': request.data.get('filter_mobile_code'),
            'filter_tag': request.data.get('filter_tag'),
            'end_time': request.data.get('end_time'),
            'celery_task_id': task_id
        }

        serializer = MailingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            exp = datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M:%S')
            result = send_message.apply_async([serializer.data['id']], eta=data['start_time'], expires=exp, task_id=task_id)
            logger.info(f'Task Result: {result}')

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MailingItemApiView(ObjectDetailsApiView):
    def get(self, request, mailing_id, *args, **kwargs):
        """Get mailing data by mailing id"""
        return ObjectDetailsApiView.get(self, request, mailing_id, Mailing, MailingSerializer)

    def put(self, request, mailing_id, *args, **kwargs):
        """Modify mailing data by mailing id, revoke current task and re-schedule it"""
        data = {
            'start_time': request.data.get('start_time'),
            'text': request.data.get('text'),
            'filter_mobile_code': request.data.get('filter_mobile_code'),
            'filter_tag': request.data.get('filter_tag'),
            'end_time': request.data.get('end_time')
        }

        instance = self.get_object(mailing_id, Mailing)
        if not instance:
            return Response(
                {"resp": "Object with such id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        task_id = instance.celery_task_id
        current_app.control.revoke(task_id)
        logger.info(f'Celery task with id {task_id} was revoked, will be re-scheduled soon')

        serializer = MailingSerializer(instance=instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()

            exp = datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M:%S')
            result = send_message.apply_async([serializer.data['id']], eta=data['start_time'], expires=exp, task_id=task_id)
            logger.info(f'Task Result: {result}')

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, object_id, *args, **kwargs):
        """
        Delete Mailing object,
        """
        instance = self.get_object(object_id, Mailing)
        if not instance:
            return Response(
                {"resp": "Object with such id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        current_app.control.revoke(instance.celery_task_id)
        logger.info(f'Celery task id {instance.celery_task_id} was revoked')

        instance.delete()
        return Response(
            {"resp": "Object successfully deleted"},
            status=status.HTTP_200_OK
        )


class ClientApiView(ObjectApiView):
    def get(self, request, *args, **kwargs):
        """Get all clients"""
        return ObjectApiView.get(self, Client, ClientSerializer, request)

    def post(self, request, *args, **kwargs):
        """Add new client"""
        data = {
            'phone': request.data.get('phone'),
            'mobile_code': request.data.get('mobile_code'),
            'tag': request.data.get('tag'),
            'timezone': request.data.get('timezone')
        }

        return ObjectApiView.post(self, Client, ClientSerializer, data, request)


class ClientItemApiView(ObjectDetailsApiView):
    def get(self, request, client_id, *args, **kwargs):
        """Get client data by client id"""
        return ObjectDetailsApiView.get(self, request, client_id, Client, ClientSerializer)

    def put(self, request, client_id, *args, **kwargs):
        """Modify client data by client id"""
        data = {
            'phone': request.data.get('phone'),
            'mobile_code': request.data.get('mobile_code'),
            'tag': request.data.get('tag'),
            'timezone': request.data.get('timezone')
        }

        return ObjectDetailsApiView.put(self, request, client_id, Client, ClientSerializer, data)

    def delete(self, request, client_id, *args, **kwargs):
        """Delete client from database by client id"""
        return ObjectDetailsApiView.delete(self, request, client_id, Client, ClientSerializer)


class MessageApiView(ObjectApiView):
    """Get all messages"""
    def get(self, request, *args, **kwargs):
        return ObjectApiView.get(self, Message, MessageSerializer, request)


class MessageItemApiView(ObjectDetailsApiView):
    """Get message by id"""
    def get(self, request, message_id, *args, **kwargs):
        return ObjectDetailsApiView.get(self, request, message_id, Message, MessageSerializer)
