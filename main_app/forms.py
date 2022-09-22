from django.forms import ModelForm
from .models import Profile, Chatroom
from django.contrib.auth.models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('bio',)

class ChatroomForm(ModelForm):
    class Meta:
        model = Chatroom
        fields = ('room_name',)
