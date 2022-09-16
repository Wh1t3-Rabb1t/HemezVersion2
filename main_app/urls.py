from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('chats/', views.lobby, name='lobby'),
    path('about/', views.about, name ='about'),
    path('chatrooms/', views.chatrooms, name ='chatrooms'),
    path('userpage/', views.userpage, name ='userpage'),

]