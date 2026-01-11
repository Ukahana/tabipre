from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import Favorite, FavoriteItem

class FavoritesEditView(View):
    template_name = 'mypage/favorites_edit.html'

    def get(self, request):
        favorite = Favorite.objects.filter(user=request.user).first()
        return render(request, self.template_name, {"favorite": favorite})

    def post(self, request):
        favorite = Favorite.objects.filter(user=request.user).first()

        # 入力された項目を取得
        items = request.POST.getlist("items")

        # 既存項目を削除
        favorite.items.all().delete()

        # 新しい項目を保存
        for name in items:
            if name.strip():
                FavoriteItem.objects.create(favorite=favorite, item_name=name.strip())

        messages.success(request, "お気に入りリストを更新しました。")
        return redirect("app:favorites_list")