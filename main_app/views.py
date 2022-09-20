from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.models import User

from django.db import transaction
# Importing instances of ModelForms
from .forms import UserForm, ProfileForm

# AWS-related imports
import uuid
import boto3

S3_BASE_URL = 'https://s3.ca-central-1.amazonaws.com/'
BUCKET = 'hermes-messenger'

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
    return render(request, 'chat/index.html')

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def chatrooms(request):
    return render(request, 'chatrooms.html')

@login_required
def profile(request):
    user = request.user
    user_form = UserForm()
    profile_form = ProfileForm()
    return render(request, 'profile.html', {
        'user': user,
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
@transaction.atomic
def user_update(request, user_id):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
        else:
            print(user_form.errors)
            print(profile_form.errors)
    return render(request, '')

@login_required
def add_profile_pic(request, user_id):
    # photo-file will be the "name" atrribute on the <input type = 'file'>
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            user = User.objects.get(id = user_id)
            user.profile.profile_pic = url
            user.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('profile')

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
                'type': 'chat_message',
                'message': message,
                'user': user
            }
        )

    def chat_message(self, event):
        message = event['message']
        user = event['user']

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'user': user,

        }))

