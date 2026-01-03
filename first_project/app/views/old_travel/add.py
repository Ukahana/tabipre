from django.shortcuts import render, get_object_or_404, redirect
from app.models.template import Template, TravelCategory, TravelItem
from app.models.favorite import Favorite, FavoriteItem

def add_category_and_item(request, template_id):
    template = get_object_or_404(Template, pk=template_id)

    # お気に入りリスト取得
    favorite, created = Favorite.objects.get_or_create(user=request.user)
    favorite_items = FavoriteItem.objects.filter(favorite=favorite)

    if request.method == "POST":
        category_name = request.POST.get("category_name")
        category_color = request.POST.get("category_color")
        item_name = request.POST.get("item_name")

        # 分類作成
        category = TravelCategory.objects.create(
            template=template,
            category_name=category_name,
            travel_type=1,  # CUSTOM
            category_color=category_color
        )

        # 項目作成
        TravelItem.objects.create(
            travel_category=category,
            item_name=item_name,
            item_checked=0
        )

        # 「続けますか？」モーダルを表示するためのフラグ
        return render(request, "tabipre/add_category_item.html", {
            "template": template,
            "favorite_items": favorite_items,
            "show_continue_modal": True
        })

    return render(request, "tabipre/add_category_item.html", {
        "template": template,
        "favorite_items": favorite_items,
        "show_continue_modal": False
    })