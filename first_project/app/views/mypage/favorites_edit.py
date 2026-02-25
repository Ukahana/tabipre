from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import Favorite, FavoriteItem


class FavoritesEditView(View):
    template_name = 'mypage/favorites_edit.html'

    def get(self, request):
        favorite = Favorite.objects.filter(user=request.user).first()

        if not favorite:
            favorite = Favorite.objects.create(user=request.user)

        # 既存項目をテンプレートへ渡す
        items = [item.item_name for item in favorite.items.all()]

        return render(request, self.template_name, {
            "favorite": favorite,
            "items": items,
        })

    def post(self, request):
        favorite = Favorite.objects.filter(user=request.user).first()

        if not favorite:
            favorite = Favorite.objects.create(user=request.user)

        # hidden にまとめられた items を取得
        items_raw = request.POST.get("items", "")
        items = [name for name in items_raw.split("||") if name.strip()]

        # 既存項目を削除
        favorite.items.all().delete()

        # 新しい項目を保存
        for name in items:
            FavoriteItem.objects.create(
                favorite=favorite,
                item_name=name
            )

        messages.success(request, "お気に入りを保存しました。")
        return redirect("app:favorites_list")