from django.db import models

# Create your models here.

class Chat(models.Model):
    file = models.FileField(upload_to='chats/')

class Request(models.Model):
    msg_id = models.CharField(max_length=200)
    user_id = models.CharField(max_length=200)
    user_name = models.CharField(max_length=60)
