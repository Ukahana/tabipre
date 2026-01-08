from django.urls import path

# auth
from app.views.auth import (
    RegistUserView,
    UserLoginView,
    PasswordResetMailView,
)


# home
from app.views.home import HomeView

# old_travel
from app.views.old_travel.travel_detail import travel_detail,travel_uncheck_all,toggle_item_checked
from app.views.old_travel.template_edit import template_edit
from app.views.old_travel.add import add_category_and_item
from app.views.old_travel.link import create_link
from app.views.old_travel.old_travel_edit1 import old_travel_edit1
from app.views.old_travel.old_travel_edit2 import old_travel_edit2

# new_travel
from app.views.new_travel.travel_step import (
    travel_create_step1,
    travel_step2 as new_travel_step2,
)
from app.views.new_travel.template_edit2 import (
    template_edit2,
    old_template_edit,
)
from app.views.new_travel.add_category_item import add_category_item
from app.views.new_travel.autocomplete_category_item import (
    autocomplete_category,
    autocomplete_item,
)
from app.views.new_travel.step_copy import (
    TravelCopyModalView,
    TravelCopyApplyView,
)
from app.views.new_travel.step_template import TemplateCreateView

app_name = 'app'
urlpatterns = [
    # ログイン
    path('regist/',RegistUserView.as_view(),name='regist'),
    path('',UserLoginView.as_view(),name='user_login'),
    path('login/',UserLoginView.as_view(),name='user_login'),
    path('password_reset/',PasswordResetMailView.as_view(),name='password_reset'),
    
    # ホーム
    path('home/', HomeView.as_view(), name='home'),
    

    # 分類・項目編集
    path("category/<int:category_id>/add/", add_category_and_item, name="add_category_and_item"),
    
    
    # 新規テンプレート作成
    path('travel_step1/', travel_create_step1, name='travel_step1'),
    path('travel_step2/', new_travel_step2, name='travel_step2'), 
    path("template/<int:template_id>/edit/", template_edit, name="template_edit"),
    path("template/<int:template_id>/edit2/",template_edit2,name="template_edit2"),
    path("template/<int:template_id>/add/",add_category_item,name="add_category_item"),
    path("autocomplete/category/", autocomplete_category, name="autocomplete_category"),
    path("autocomplete/item/", autocomplete_item, name="autocomplete_item"),
    path('template/<int:template_id>/old_edit/',old_template_edit,name='old_template'),

    # 過去テンプレート編集
    # 旅行詳細
    path("travel/<int:travel_id>/",travel_detail, name="travel_detail"),
    path("item/<int:item_id>/toggle/", toggle_item_checked, name="toggle_item_checked"),
    path("travel/<int:travel_id>/uncheck_all/", travel_uncheck_all, name="travel_uncheck_all"),
    path("travel/<int:travel_id>/link/", create_link, name="travel_link"),
    path("travel/<int:travel_id>/old_edit1/", old_travel_edit1, name="old_travel_edit1"),
    path("travel/<int:travel_id>/old_edit2/", old_travel_edit2, name="old_travel_edit2"),
    path('template/create/', TemplateCreateView, name='template_create'),
    path('travel/copy/modal/', TravelCopyModalView, name='travel_copy_modal'),
]

