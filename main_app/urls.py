from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('chats/', views.lobby, name='lobby'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('about/', views.about, name ='about'),
    path('chatrooms/', views.chatrooms, name ='chatrooms'),
    path('profile/', views.profile, name ='profile'),
    path('users/<int:user_id>/update/', views.user_update, name='user_update'),
    path('users/<int:user_id>/add_profile_pic/', views.add_profile_pic, name='add_profile_pic'),
    path('accounts/signup/', views.signup , name='signup'),

]




