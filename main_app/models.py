from django.db import models
from datetime import date
from django.contrib.auth.models import User
# Create your models here.



# CHATROOM
class Chatroom(models.Model):
    host_id = models.ForeignKey(User, on_delete = models.CASCADE)
    room_name = models.CharField(max_length=100)


    def __str__(self):
        return self.room_name
    
    class Meta:
        ordering =['room_name']


# MESSAGE
class Message(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    chat_id = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    message_body = models.TextField(max_length=255)

    def __str__(self):
        return self.message_body


