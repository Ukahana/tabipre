from django.urls import path
from.views import (
    RegistUserView,UserLoginView,
    PasswordResetMailView,TravelStep1View,TravelStep2View,
    HomeView
)


app_name = 'app'
urlpatterns = [
    path('regist/',RegistUserView.as_view(),name='regist'),
    path('',UserLoginView.as_view(),name='user_login'),
    path('login/',UserLoginView.as_view(),name='user_login'),
    path('password_reset/',PasswordResetMailView.as_view(),name='password_reset'),
    path('home/', HomeView.as_view(), name='home'),
    path('travel_step1/', TravelStep1View, name='travel_step1'),
    path('travel_step2/', TravelStep2View, name='travel_step2'),

]

