from django.urls import path
from.views import (
    RegistUserView,HomeView,UserLoginView,UserlogoutView
)


app_name = 'app'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('home/',HomeView.as_view(),name='home'),
    path('regist/',RegistUserView.as_view(),name='regist'),
    path('user_login/',UserLoginView.as_view(),name='user_login'),
    path('user_logout/',UserlogoutView.as_view(),name='user_logout'),
]

