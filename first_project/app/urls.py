from django.urls import path
from .views import (
    RegistUserView, UserLoginView, PasswordResetMailView,
    HomeView,
    travel_detail, template_edit, edit_item, add_item, add_category_and_item,
      travel_create_step1, travel_create_step2,
    TemplateCreateView, TravelCopyModalView, TravelCopyApplyView,
)


app_name = 'app'
urlpatterns = [
    # ログイン
    path('regist/',RegistUserView.as_view(),name='regist'),
    path('',UserLoginView.as_view(),name='user_login'),
    path('login/',UserLoginView.as_view(),name='user_login'),
    path('password_reset/',PasswordResetMailView.as_view(),name='password_reset'),
    
    # ホーム
    path('home/', HomeView.as_view(), name='home'),
    
    # 既存のテンプレート編集
    path("travel/<int:travel_id>/",travel_detail, name="travel_detail"),
    path("travel/<int:travel_id>/edit/",template_edit, name="template_edit"),
    path("item/<int:item_id>/edit/", edit_item, name="edit_item"),
    path("category/<int:category_id>/item/add/", add_item, name="add_item"),
    path("template/<int:template_id>/add_category_item/",add_category_and_item,name="add_category_item"),
    
    # 新規テンプレート作成
    path('travel_step1/', travel_create_step1, name='travel_step1'),
    path('travel_step2/<int:travel_id>/', travel_create_step2, name='travel_step2'),
    path('template/create/', TemplateCreateView, name='template_create'),
    path('travel/copy/modal/', TravelCopyModalView, name='travel_copy_modal'),
    path('travel/copy/<int:travel_id>/', TravelCopyApplyView, name='travel_copy'),


]

