from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Profile, Chatroom, Message
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from django.db import transaction
# Importing instances of ModelForms

from .forms import UserForm, ProfileForm, ChatroomForm

# AWS-related imports
import uuid
import boto3

S3_BASE_URL = 'https://s3.ca-central-1.amazonaws.com/'
BUCKET = 'hermes-messenger'

# Import the login_required decorator

#  for class based authorization

# for chat


# Create your views here.

@login_required
def room(request, room_name):
    chatrooms = Chatroom.objects.all()
    chatroom = Chatroom.objects.all().filter(id = room_name)[0]

    print(chatroom.id)
    messages = Message.objects.all().filter(chat_id_id=room_name)

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'chatrooms': chatrooms,
        'current_room': chatroom,
        'messages': messages
    })


def home(request):
    return render(request, 'home.html', {
        'name': 'Home'
    })


def about(request):
    return render(request, 'about.html', {
        'name': 'About Hermes Messenger App',
    })


@login_required
def lobby(request):
    chatrooms = Chatroom.objects.filter(host=request.user.id)
    return render(request, 'chat/index.html', {
        'chatrooms': chatrooms,
        'name': 'Your Chatrooms',
    })


@login_required
def profile(request):
    chatrooms = Chatroom.objects.all()
    user = request.user
    # this should auto-fill in the user_form and profile_form instances with current User's values
    user_form = UserForm(initial={
        'email': request.user.email,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }, instance=request.user)
    profile_form = ProfileForm(initial={
        'bio': request.user.profile.bio,
    }, instance=request.user)
    return render(request, 'profile.html', {
        'chatrooms': chatrooms,
        'name': 'User Profile',
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
    chatrooms = Chatroom.objects.all()
    return render(request, '', {
        'chatrooms': chatrooms,
    })


@login_required
def add_profile_pic(request, user_id):
    # photo-file will be the "name" atrribute on the <input type = 'file'>
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            user = User.objects.get(id=user_id)
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
    context = {
        'form': form,
        'error_message': error_message,
        'name': 'Sign Up'
    }
    return render(request, 'registration/signup.html', context)


@login_required
def create_room(request):
    if request.method == "POST":
        chatroom_form = ChatroomForm(request.POST)
        photo_file = request.FILES.get('photo-file', None)
        if photo_file:
            s3 = boto3.client('s3')
            key = uuid.uuid4().hex[:6] + \
                photo_file.name[photo_file.name.rfind('.'):]
            try:
                s3.upload_fileobj(photo_file, BUCKET, key)
                url = f"{S3_BASE_URL}{BUCKET}/{key}"
            except:
                print('An error occurred uploading file to S3')
        else:
            url = 'https://i.imgur.com/efLA0Or.jpeg'
        if chatroom_form.is_valid():
            new_chatroom = chatroom_form.save(commit=False)
            new_chatroom.host_id = request.user.id
            new_chatroom.chat_pic = url
            new_chatroom.save()
            return redirect('lobby')
        else:
            print(chatroom_form.errors)
    # the following is for GET requests
    chatroom_form = ChatroomForm()
    chatrooms = Chatroom.objects.all()
    return render(request, 'main_app/chatroom_create.html', {
        'chatrooms': chatrooms,
        'chatroom_form': chatroom_form,
        'name': 'Create Chatroom'
    })


@login_required
def add_chatroom_pic(request, user_id):
    # photo-file will be the "name" atrribute on the <input type = 'file'>
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            user = User.objects.get(id=user_id)
            user.profile.profile_pic = url
            user.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('profile')


class UpdateRoom(LoginRequiredMixin, UpdateView):
    model = Chatroom
    fields = ['room_name', ]


class DeleteRoom(LoginRequiredMixin, DeleteView):
    model = Chatroom
    success_url = '/chat/'
