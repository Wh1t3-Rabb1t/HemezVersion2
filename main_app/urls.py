from django.urls import path
from . import views

from django.urls import re_path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('chats/', views.lobby, name='lobby'),
    path('about/', views.about, name ='about'),
    path('chatrooms/', views.chatrooms, name ='chatrooms'),
    path('profile/', views.profile, name ='profile'),
    path('users/<int:user_id>/update/', views.user_update, name='user_update'),
    path('users/<int:user_id>/add_profile_pic/', views.add_profile_pic, name='add_profile_pic'),
    path('accounts/signup/', views.signup , name='signup'),

]




websocket_urlpatterns = [
    re_path(r'ws/socket-server/', views.ChatConsumer.as_asgi())
]