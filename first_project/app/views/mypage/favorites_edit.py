from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import Favorite, FavoriteItem
from app.forms.favorite import FavoriteItemsForm 


class FavoritesEditView(View):
    template_name = 'mypage/favorites_edit.html'

    def get(self, request):
        favorite = Favorite.objects.filter(user=request.user).first()

        if not favorite:
            favorite = Favorite.objects.create(user=request.user)

        # 既存項目をフォームに渡す（JS で hidden に入れる前提）
        items = [item.item_name for item in favorite.items.all()]
        form = FavoriteItemsForm(initial={"items": "||".join(items)})

        return render(request, self.template_name, {
            "favorite": favorite,
            "form": form,
        })

    def post(self, request):
        favorite = Favorite.objects.filter(user=request.user).first()

        if not favorite:
            favorite = Favorite.objects.create(user=request.user)

        form = FavoriteItemsForm(request.POST)

        if not form.is_valid():
            # エラー時は元の画面に戻す
            return render(request, self.template_name, {
                "favorite": favorite,
                "form": form,
            })

        # バリデーション済みの items を取得
        items = form.cleaned_data["items"]

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