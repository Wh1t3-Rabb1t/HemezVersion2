from django.shortcuts import render,redirect
from django.contrib.auth import login

from django.contrib.auth.forms import UserCreationForm

# Import the login_required decorator
from django.contrib.auth.decorators import login_required

#  for class based authorization
from django.contrib.auth.mixins import LoginRequiredMixin

# for chat 
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


# Create your views here.
def lobby(request):
    return render(request, 'lobby.html')

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def chatrooms(request):
  return render(request, 'chatrooms.html')

def userpage(request):
  return render(request, 'userpage.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('/')
    else:
      print(form.errors)
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)








# CHAT FEATURES CHANNELS
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
   

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json['message']
        user = text_data_json['user']
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'user':user
            }
        )

    def chat_message(self, event):
        message = event['message']
        user = event['user']

        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message,
            'user':user,

        }))