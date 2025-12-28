from django.urls import path
from.views import (
    RegistUserView,HomeView,UserLoginView,UserView,PassWord_Reset
)


app_name = 'app'
urlpatterns = [
    path('home/',HomeView.as_view(),name='home'),
    path('regist/',RegistUserView.as_view(),name='regist'),
    path('',UserLoginView.as_view(),name='user_login'),
    path('user/',UserView.as_view(),name='user'),
    path('password_reset/',PassWord_Reset.as_view(),name='passwprd_reset'),
    
]

