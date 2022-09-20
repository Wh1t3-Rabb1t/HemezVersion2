from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('chats/', views.lobby, name='lobby'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('about/', views.about, name ='about'),
    path('chatrooms/', views.chatrooms, name ='chatrooms'),
    path('userpage/', views.userpage, name ='userpage'),
    path('accounts/signup/', views.signup , name='signup'),

]




