from django.urls import path
from.views import (
    RegistUserView,UserLoginView,
    PasswordResetMailView
)


app_name = 'app'
urlpatterns = [
    path('regist/',RegistUserView.as_view(),name='regist'),
    path('',UserLoginView.as_view(),name='user_login'),
    path('password_reset/',PasswordResetMailView.as_view(),name='password_reset'),
    
]

