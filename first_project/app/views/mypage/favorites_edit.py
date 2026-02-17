from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import Favorite, FavoriteItem

class FavoritesEditView(View):
    template_name = 'mypage/favorites_edit.html'

    def get(self, request):
        favorite = Favorite.objects.filter(user=request.user).first()

        # 万が一 Favorite が存在しない場合は作成
        if not favorite:
            favorite = Favorite.objects.create(user=request.user)

        return render(request, self.template_name, {"favorite": favorite})

    def post(self, request):
        favorite = Favorite.objects.filter(user=request.user).first()

        if not favorite:
            favorite = Favorite.objects.create(user=request.user)

        # 入力された項目を取得
        items = request.POST.getlist("items")

        # 既存項目を削除
        favorite.items.all().delete()

        # 新しい項目を保存（空欄は除外）
        for name in items:
            cleaned = name.strip()
            if cleaned:
                FavoriteItem.objects.create(
                    favorite=favorite,
                    item_name=cleaned
                )

        return redirect("app:favorites_list")