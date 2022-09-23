from django.db import models
from datetime import date, datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# class Profile extends the User model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    join_date = models.DateField(default = date.today)
    bio = models.TextField(max_length=500)
    profile_pic = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username

    # this will create a Profile instance whenever a new User is created/signs up
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


# CHATROOM
class Chatroom(models.Model):
    host = models.ForeignKey(User, on_delete = models.CASCADE)
    room_name = models.CharField(max_length=100)
    chat_pic = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.room_name
    
    class Meta:
        ordering =['room_name']
    
    def get_absolute_url(self):
        return reverse('room', kwargs={'room_name': self.room_name})


# MESSAGE
class Message(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    username = models.CharField(max_length=100)
    chat_id = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    message_body = models.TextField(max_length=255)

    def __str__(self):
        return self.message_body

    
