from django.db import models
from pytz import common_timezones


class Mailing(models.Model):
    id = models.AutoField(primary_key=True)
    start_time = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True)
    text = models.CharField(max_length=500)
    filter_mobile_code = models.CharField(max_length=3, blank=True, default='')
    filter_tag = models.CharField(max_length=20, blank=True, default='')
    end_time = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True)

    def __str__(self):
        return f'{self.id}, {self.text[:15]}, {self.filter_mobile_code}, {self.filter_tag}'


class Client(models.Model):
    TIMEZONES = tuple(zip(common_timezones, common_timezones))

    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11)
    mobile_code = models.CharField(max_length=3)
    tag = models.CharField(max_length=20)
    timezone = models.CharField(max_length=50, choices=TIMEZONES, blank=True, null=True)

    def __str__(self):
        return f'{self.id}, {self.phone}, {self.mobile_code}, {self.tag}'


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    send_time = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True)
    status = models.BooleanField(default=False)
    id_mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}, {self.send_time}, {self.status}'