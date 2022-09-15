from django.contrib import admin
from .models import User, Chatroom, Message, Join_table

# Register your models here.
admin.site.register(User)
admin.site.register(Chatroom)
admin.site.register(Message)
admin.site.register(Join_table)