from unicodedata import name
from django.urls import URLPattern, path

from base.views import create_room, delete_message, home,registerUser ,login_page, logout_page, room, update_room, delete_room

urlpatterns = [
    path('',home,name = 'home'),
    path('login', login_page,name= 'login'),
    path('register', registerUser,name= 'register'),
    path('logout' , logout_page,name= 'logout'),
    path('room/<str:pk>',room, name = 'room'),
    path('create-room',create_room,name = 'create-room'),
    path('update-room/<str:pk>',update_room,name = 'update-room'),
    path('delete-room/<str:pk>',delete_room,name = 'delete-room'),
    path('delete-message/<str:pk>',delete_message,name = 'delete-message')
]