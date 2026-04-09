from django.urls import path
from django.contrib.auth import logout
from django.shortcuts import redirect

# portfolio
from app.views.portfolio import(
    PortfolioTopView,
)
# auth
from app.views.auth import (
    RegistUserView,
    UserLoginView,
    PasswordResetMailView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)

# home
from app.views.home import HomeView

# old_travel
from app.views.old_travel.travel_detail import (
    travel_detail,
    travel_uncheck_all,
    toggle_item_checked,
)
from app.views.old_travel.template_manage import (
    old_template_edit,
    add_item_page,
    edit_item,
)
from app.views.old_travel.add import category_item_add
from app.views.old_travel.old_travel_edit import (
    old_travel_edit1,
    old_travel_edit2,
)

# new_travel
from app.views.new_travel.travel_step import (
    travel_create_step1,
    travel_step2 as new_travel_step2,
)
from app.views.new_travel.template_edit import template_edit
from app.views.new_travel.template_edit2 import template_edit2
from app.views.new_travel.old_template_copy import old_template_copy
from app.views.new_travel.add_category_item import add_category_item
from app.views.new_travel.autocomplete_category_item import (
    autocomplete_category,
    autocomplete_item,
)
from app.views.new_travel.step_copy import (
    TravelCopyModalView,
)
from app.views.new_travel.step_template import TemplateCreateView

# mypage
from app.views.mypage.mypage import mypage
from app.views.mypage.favorites_list import favorites_list
from app.views.mypage.link import (
    share_settings,
    update_share_link,
    delete_share_link,
)
from app.views.mypage.password_change import CustomPasswordChangeView
from app.views.mypage.account_edit import AccountEditView, EmailChangeView
from app.views.mypage.favorites_edit import FavoritesEditView

# old_travel link
from app.views.old_travel.copylink import (
    toggle_item_checked_share
)
from app.views.old_travel.create_link import (
    create_link
)
from app.views.old_travel.share_view import (
    share_view,
    share_edit_view,
    share_add_category_item
)


def user_logout(request):
    logout(request)
    next_url = request.GET.get("next")
    if next_url:
        return redirect(next_url)
    return redirect('app:login')


app_name = 'app'

urlpatterns = [
    path('', PortfolioTopView.as_view(), name='portfolio_top'),
    # ============================
    # 認証（Auth）
    # ============================
    path('tabipre/login/', UserLoginView.as_view(), name='login'),
    path('tabipre/logout/', user_logout, name='logout'),
    path('tabipre/regist/', RegistUserView.as_view(), name='regist'),

    # パスワード再設定
    path('tabipre/password_reset/', PasswordResetMailView.as_view(), name='password_reset'),
    # パスポート再設定メールのリンク
    path(
       'tabipre/reset/<uidb64>/<token>/',
       CustomPasswordResetConfirmView.as_view(),
       name='password_reset_confirm'
    ),


    path('tabipre/reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # ============================
    # 共有リンク（管理画面：IDベース）
    # ============================
    path('tabipre/share/settings/', share_settings, name='share_settings'),
    path('tabipre/share/<str:token>/update/', update_share_link, name='share_update'),
    path('tabipre/share/<str:token>/delete/', delete_share_link, name='delete_share_link'),

    # ============================
    # 共有リンク（公開：tokenベース）
    # ============================
    path("tabipre/share/<str:token>/", share_view, name="share_view"),
    path("tabipre/share/<str:token>/edit/", share_edit_view, name="share_edit_view"),
    path("tabipre/share/<str:token>/edit/add/", share_add_category_item, name="share_add_category_item"),
    path("tabipre/share/<str:token>/toggle_item/<int:item_id>/", toggle_item_checked_share, name="toggle_item_checked_share"),


    # ============================
    # ホーム
    # ============================
    path('tabipre/home/', HomeView.as_view(), name='home'),


    # ============================
    # 新規旅行（New Travel）
    # ============================
    path('tabipre/travel_step1/', travel_create_step1, name='travel_step1'),
    path('tabipre/travel_step2/', new_travel_step2, name='travel_step2'),

    path("tabipre/template/<int:template_id>/edit/", template_edit, name="template_edit"),
    path("tabipre/template/<int:template_id>/edit2/", template_edit2, name="template_edit2"),
    path("tabipre/template/<int:template_id>/add/", add_category_item, name="add_category_item"),

    path("tabipre/autocomplete/category/", autocomplete_category, name="autocomplete_category"),
    path("tabipre/autocomplete/item/", autocomplete_item, name="autocomplete_item"),

    path('tabipre/template/<int:template_id>/old_copy/', old_template_copy, name='old_template_copy'),
    path('tabipre/template/create/', TemplateCreateView, name='template_create'),

    path('tabipre/travel/copy/modal/', TravelCopyModalView, name='travel_copy_modal'),


    # ============================
    # 旧旅行（Old Travel）
    # ============================
    path("tabipre/travel/<int:travel_id>/", travel_detail, name="travel_detail"),

    path("tabipre/old_template/<int:template_id>/edit/", old_template_edit, name="old_template_edit"),
    path("tabipre/old_template/<int:template_id>/add/", category_item_add, name="category_item_add"),

    path("tabipre/item/add/<int:template_id>/", add_item_page, name="add_item_page"),
    path("tabipre/item/edit/", edit_item, name="edit_item"),
    path("tabipre/toggle_item/<int:item_id>/", toggle_item_checked, name="toggle_item"),
    path("tabipre/travel/<int:travel_id>/uncheck_all/", travel_uncheck_all, name="travel_uncheck_all"),

    path("tabipre/travel/<int:travel_id>/old_edit1/", old_travel_edit1, name="old_travel_edit1"),
    path("tabipre/travel/<int:travel_id>/old_edit2/", old_travel_edit2, name="old_travel_edit2"),

    # 共有リンク作成
    path("tabipre/travel/<int:travel_id>/link/", create_link, name="travel_link"),


    # ============================
    # マイページ（MyPage）
    # ============================
    path('tabipre/mypage/', mypage, name='mypage'),
    path('tabipre/favorites/', favorites_list, name='favorites_list'),
    path('tabipre/favorites/edit/', FavoritesEditView.as_view(), name='favorites_edit'),

    path('tabipre/account/password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('tabipre/account/edit/', AccountEditView.as_view(), name='account_edit'),
    path('tabipre/account/email/', EmailChangeView.as_view(), name='account_email'),
]