from django.shortcuts import render, get_object_or_404, redirect
from ...models.travel import Travel_info
from ...models.template import Template, TravelCategory, TravelItem
from ...models.favorite import Favorite, FavoriteItem

def template_edit(request, template_id):
    template = get_object_or_404(Template, id=template_id)

    return render(request, "new_travel/template_edit.html", {
        "template": template
    })


    # お気に入りリスト（後で作成して修正する）
    favorite, created = Favorite.objects.get_or_create(user=request.user)
    favorite_items = FavoriteItem.objects.filter(favorite=favorite)
    
    context = {
        "travel": travel,
        "template": template,
        "categories": categories,
        "favorite_items": favorite_items,
    }

    return render(request, "tabipre/template_edit.html", context)
# 項目編集
def edit_item(request, item_id):
    item = get_object_or_404(TravelItem, pk=item_id)

    if request.method == "POST":
        new_name = request.POST.get("item_name")
        if "delete" in request.POST:
            item.delete()
        else:
            item.item_name = new_name
            item.save()

        return redirect("app:template_edit", travel_id=item.travel_category.template.travel_info_id)

    return render(request, "tabipre/edit_item_modal.html", {"item": item})

def add_item(request, category_id):
    category = get_object_or_404(TravelCategory, pk=category_id)

    if request.method == "POST":
        name = request.POST.get("item_name")
        add_favorite = request.POST.get("favorite") == "on"

        # TravelItem に追加
        TravelItem.objects.create(
            travel_category=category,
            item_name=name,
            item_checked=0
        )

        # 項目追加モーダル
        if add_favorite:
            favorite, created = Favorite.objects.get_or_create(user=request.user)
            FavoriteItem.objects.create(
                favorite=favorite,
                item_name=name
            )

        return redirect("app:template_edit", travel_id=category.template.travel_info_id)

    return render(request, "tabipre/add_item_modal.html", {"category": category})