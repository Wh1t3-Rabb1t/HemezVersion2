from django.urls import path
from . import views


urlpatterns = [

    # MAIN URLS
    path('', views.home, name='home'),
    path('about/', views.about, name ='about'),
    path('profile/', views.profile, name ='profile'),

    # USER URLS
    path('users/<int:user_id>/update/', views.user_update, name='user_update'),
    path('users/<int:user_id>/add_profile_pic/', views.add_profile_pic, name='add_profile_pic'),
    path('accounts/signup/', views.signup , name='signup'),

    #CHAT URLS
    # use 'lobby' as index view, with href links to edit and delete
    path('chat/', views.lobby, name='lobby'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('chatroom/create',views.create_room, name='create_room'),
    path('chatroom/<int:pk>/update/', views.UpdateRoom.as_view(), name='chatroom_update'),
    path('chatroom/<int:pk>/delete/', views.DeleteRoom.as_view(), name='chatroom_delete'),
]
