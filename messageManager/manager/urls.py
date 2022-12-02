from django.urls import path
from .views import index, MailingApiView, ClientApiView, MessageApiView, MailingItemApiView

app_name = 'manager'

urlpatterns = [
    path('', index),
    path('api/mailings', MailingApiView.as_view()),
    path('api/mailing/<int:mailing_id>/', MailingItemApiView.as_view()),
    path('api/clients', ClientApiView.as_view()),
    path('api/messages', MessageApiView.as_view())
]
