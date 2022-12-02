from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MessageSerializer, ClientSerializer, MailingSerializer
from .models import Message, Client, Mailing


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

    def put(self, request, object_id, model, model_serializer, data, *args, **kwargs):
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
                {"resp": "Mailing object with such id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        instance.delete()
        return Response(
            {"resp": "Object successfully deleted"},
            status=status.HTTP_200_OK
        )


class MailingApiView(ObjectApiView):
    def get(self, request, *args, **kwargs):
        return ObjectApiView.get(self, Mailing, MailingSerializer, request)

    def post(self, request, *args, **kwargs):

        data = {
            'id': request.data.get('id'),
            'start_time': request.data.get('start_time'),
            'text': request.data.get('text'),
            'filter': request.data.get('filter'),
            'end_time': request.data.get('end_time')
        }

        return ObjectApiView.post(self, Mailing, MailingSerializer, data, request)


class MailingItemApiView(ObjectDetailsApiView):
    def get(self, request, mailing_id, *args, **kwargs):
        return ObjectDetailsApiView.get(self, request, mailing_id, Mailing, MailingSerializer)

    def put(self, request, mailing_id, *args, **kwargs):

        data = {
            'start_time': request.data.get('start_time'),
            'text': request.data.get('text'),
            'filter': request.data.get('filter'),
            'end_time': request.data.get('end_time')
        }

        return ObjectDetailsApiView.put(self, request, mailing_id, Mailing, MailingSerializer, data)

    def delete(self, request, mailing_id, *args, **kwargs):
        return ObjectDetailsApiView.delete(self, request, mailing_id, Mailing, MailingSerializer)


class ClientApiView(ObjectApiView):
    def get(self, request, *args, **kwargs):
        return ObjectApiView.get(self, Client, ClientSerializer, request)

    def post(self, request, *args, **kwargs):
        data = {
            'phone': request.data.get('phone'),
            'mobile_code': request.data.get('mobile_code'),
            'tag': request.data.get('tag'),
            'timezone': request.data.get('timezone')
        }

        return ObjectApiView.post(self, Client, ClientSerializer, data, request)


class ClientItemApiView(ObjectDetailsApiView):
    def get(self, request, client_id, *args, **kwargs):
        return ObjectDetailsApiView.get(self, request, client_id, Client, ClientSerializer)

    def put(self, request, client_id, *args, **kwargs):
        data = {
            'phone': request.data.get('phone'),
            'mobile_code': request.data.get('mobile_code'),
            'tag': request.data.get('tag'),
            'timezone': request.data.get('timezone')
        }

        return ObjectDetailsApiView.put(self, request, client_id, Client, ClientSerializer, data)

    def delete(self, request, client_id, *args, **kwargs):
        return ObjectDetailsApiView.delete(self, request, client_id, Client, ClientSerializer)


class MessageApiView(ObjectApiView):
    def get(self, request, *args, **kwargs):
        return ObjectApiView.get(self, Message, MessageSerializer, request)


class MessageItemApiView(ObjectDetailsApiView):
    def get(self, request, message_id, *args, **kwargs):
        return ObjectDetailsApiView.get(self, request, message_id, Message, MessageSerializer)

    # def delete(self, request, message_id, *args, **kwargs):
    #     return ObjectDetailsApiView.delete(self, request, message_id, Message, MessageSerializer)
