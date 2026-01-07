from django.urls import path
from .views import (
    RegistUserView, UserLoginView, PasswordResetMailView,
    HomeView,
    travel_detail, template_edit, edit_item, add_item, add_category_and_item,
      travel_create_step1, travel_step2,
    TemplateCreateView, TravelCopyModalView, template_edit2,
    add_category_item,autocomplete_category,autocomplete_item,
    old_template_edit
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
    # 旅行詳細
    path("travel/<int:travel_id>/",travel_detail, name="travel_detail"),
    # テンプレート編集
    path("travel/<int:template_id>/", template_edit, name="travel_edit"),
    # 分類・項目編集
    path("category/<int:category_id>/item/add/", add_item, name="add_item"),
    
    
    # 新規テンプレート作成
    path('travel_step1/', travel_create_step1, name='travel_step1'),
    path('travel_step2/', travel_step2, name='travel_step2'), 
    path("template/<int:template_id>/edit/", template_edit, name="template_edit"),
    path("template/<int:template_id>/edit2/",template_edit2,name="template_edit2"),
    path("template/<int:template_id>/add/",add_category_item,name="add_category_item"),
    path("autocomplete/category/", autocomplete_category, name="autocomplete_category"),
    path("autocomplete/item/", autocomplete_item, name="autocomplete_item"),
    path('template/<int:template_id>/old_edit/',old_template_edit,name='old_template'),

    # 過去テンプレート作成
    path('template/create/', TemplateCreateView, name='template_create'),
    path('travel/copy/modal/', TravelCopyModalView, name='travel_copy_modal'),
]

