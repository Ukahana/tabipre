from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ...models import Favorite

@login_required
def favorites_list(request):
    # ユーザーの Favorite を1つ取得（なければ新規作成）
    favorite, created = Favorite.objects.get_or_create(user=request.user)

    # FavoriteItem の一覧を取得
    favorite_items = favorite.items.all()

    return render(request, 'mypage/favorites_list.html', {
        'favorite_items': favorite_items
    })