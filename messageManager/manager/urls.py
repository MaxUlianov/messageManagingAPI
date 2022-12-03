from django.urls import path, reverse
from .views import index, MailingApiView, ClientApiView, MessageApiView, MailingItemApiView
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

app_name = 'manager'

urlpatterns = [
    path('', index),
    path('api/mailings', MailingApiView.as_view()),
    path('api/mailing/<int:mailing_id>/', MailingItemApiView.as_view()),
    path('api/clients', ClientApiView.as_view()),
    path('api/messages', MessageApiView.as_view()),
    path('openapi', get_schema_view(
            title="messageManager",
            description="",
            version="1.0.0"
        ), name='openapi-schema'),
    path('docs/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui')
]
