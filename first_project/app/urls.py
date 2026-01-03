from django.urls import path
from.views import (
    RegistUserView,UserLoginView,
    PasswordResetMailView,TravelStep1View,TravelStep2View,
    HomeView,travel_detail,template_edit, edit_item, add_item,add_category_and_item
)


app_name = 'app'
urlpatterns = [
    path('regist/',RegistUserView.as_view(),name='regist'),
    path('',UserLoginView.as_view(),name='user_login'),
    path('login/',UserLoginView.as_view(),name='user_login'),
    path('password_reset/',PasswordResetMailView.as_view(),name='password_reset'),
    path('home/', HomeView.as_view(), name='home'),
    path("travel/<int:travel_id>/",travel_detail, name="travel_detail"),
    path("travel/<int:travel_id>/edit/",template_edit, name="template_edit"),
    path("item/<int:item_id>/edit/", edit_item, name="edit_item"),
    path("category/<int:category_id>/item/add/", add_item, name="add_item"),
    path("template/<int:template_id>/add_category_item/",add_category_and_item,name="add_category_item"),
    
    path('travel_step1/', TravelStep1View, name='travel_step1'),
    path('travel_step2/', TravelStep2View, name='travel_step2'),
    

]

