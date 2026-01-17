from django.urls import path

from django.contrib.auth import logout
from django.shortcuts import redirect

# auth
from app.views.auth import (
    RegistUserView,
    UserLoginView,
    PasswordResetMailView,
)

# home
from app.views.home import HomeView

# old_travel
from app.views.old_travel.travel_detail import (
    travel_detail,
    travel_uncheck_all,
    toggle_item_checked,
)
from app.views.old_travel.template_manage import old_template_edit,add_item_page,edit_item,delete_template

from app.views.old_travel.add import category_item_add
from app.views.old_travel.old_travel_edit1 import old_travel_edit1
from app.views.old_travel.old_travel_edit2 import old_travel_edit2

# new_travel
from app.views.new_travel.travel_step import (
    travel_create_step1,
    travel_step2 as new_travel_step2,
)
from app.views.new_travel.template_edit2 import (
    template_edit,
    old_template_copy,
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

from app.views.mypage.mypage import mypage
from app.views.mypage.favorites_list import favorites_list
from app.views.mypage.link import (
    share_settings,
    update_share_link,
    delete_share_link,
)
from app.views.mypage.account_edit import AccountEditView
from app.views.mypage.password_change import CustomPasswordChangeView
from app.views.mypage.favorites_edit import FavoritesEditView
from app.views.old_travel.link import create_link,share_view

def user_logout(request):
    logout(request)
    return redirect('app:login')

app_name = 'app'
urlpatterns = [
    # ログイン
    path('logout/', user_logout, name='logout'),
    path('', UserLoginView.as_view(), name='login'),
    path('regist/', RegistUserView.as_view(), name='regist'),
    path('password_reset/',PasswordResetMailView.as_view(),name='password_reset'),
    
    # ホーム
    path('home/', HomeView.as_view(), name='home'),
    
    
    # 新規テンプレート作成
    path('travel_step1/', travel_create_step1, name='travel_step1'),
    path('travel_step2/', new_travel_step2, name='travel_step2'), 
    path("template/<int:template_id>/edit/",template_edit,name="template_edit"),
    path("template/<int:template_id>/add/",add_category_item,name="add_category_item"),
    path("autocomplete/category/", autocomplete_category, name="autocomplete_category"),
    path("autocomplete/item/", autocomplete_item, name="autocomplete_item"),
    path('template/<int:template_id>/old_copy/',old_template_copy,name='old_template_copy'),

    # マイページ
    path('mypage/', mypage, name='mypage'),
    # お気に入り
    path('favorites/',favorites_list, name='favorites_list'),
    path('favorites/edit/', FavoritesEditView.as_view(), name='favorites_edit'),

    # 共有リンク
    path('share/settings/', share_settings, name='share_settings'),
    path('share/<int:link_id>/update/', update_share_link, name='share_update'),
    path('share/<int:link_id>/delete/', delete_share_link, name='delete_share_link'),   
    path('account/edit/', AccountEditView.as_view(),  name='account_edit'),
    # パスワード変更
    path('account/password_change/', CustomPasswordChangeView.as_view(), name='password_change'),


    # 過去テンプレート編集
    # 旅行詳細
    path("travel/<int:travel_id>/",travel_detail, name="travel_detail"),
    path("old_template/<int:template_id>/edit/", old_template_edit,name="old_template_edit"),
    # 分類・項目の追加画面
    path("old_template/<int:template_id>/add/", category_item_add, name="category_item_add"), 
    path("item/add/<int:template_id>/", add_item_page, name="add_item_page"),
    # 項目名を編集
    path("item/edit/<int:item_id>/", edit_item, name="edit_item"),
    # 旅行情報を削除
    path('old_template/<int:template_id>/delete/',delete_template,name='delete_template'),
    # リンクの作成
    # 共有リンク
    path("travel/<int:travel_id>/link/", create_link, name="travel_link"),
    path("share/<str:token>/", share_view, name="share_view"),
    path("item/<int:item_id>/toggle/", toggle_item_checked, name="toggle_item_checked"),
    path("travel/<int:travel_id>/uncheck_all/", travel_uncheck_all, name="travel_uncheck_all"),
    path("travel/<int:travel_id>/old_edit1/", old_travel_edit1, name="old_travel_edit1"),
    path("travel/<int:travel_id>/old_edit2/", old_travel_edit2, name="old_travel_edit2"),
    path('template/create/', TemplateCreateView, name='template_create'),
    path('travel/copy/modal/', TravelCopyModalView, name='travel_copy_modal'),
    


]

