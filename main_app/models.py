from django.db import models
from datetime import date
# Create your models here.


# USER MODEL
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    join_date = models.DateField(auto_now_add=True)
    bio = models.TextField(max_length=255)
    profile_pic = models.CharField(max_length=255)

    def __str__(self):
        return self.name


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




# JOIN TABLE
class Join_table(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    chat_id = models.ForeignKey(Chatroom, on_delete = models.CASCADE)

    def __str__(self):
        return self.user_id