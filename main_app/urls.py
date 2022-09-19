from django.urls import path
from . import views

from django.urls import re_path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('chats/', views.lobby, name='lobby'),
    path('about/', views.about, name ='about'),
    path('chatrooms/', views.chatrooms, name ='chatrooms'),
    path('userpage/', views.userpage, name ='userpage'),
    path('accounts/signup/', views.signup , name='signup'),

]




websocket_urlpatterns = [
    re_path(r'ws/socket-server/', views.ChatConsumer.as_asgi())
]