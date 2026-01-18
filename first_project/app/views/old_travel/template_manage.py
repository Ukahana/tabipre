from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ...models.travel import Travel_info
from ...models.template import Template, TravelCategory, TravelItem
from ...models.favorite import Favorite, FavoriteItem


# -------------------------------
# テンプレート編集（old_template_edit）
# -------------------------------
def old_template_edit(request, template_id):
    template = get_object_or_404(Template, id=template_id)
    travel = template.travel_info

    # 分類削除（POST）
    if request.method == "POST":
        delete_cat_id = request.POST.get("delete_category")
        if delete_cat_id:
            category = get_object_or_404(TravelCategory, id=delete_cat_id)
            TravelItem.objects.filter(travel_category=category).delete()
            category.delete()
            return redirect("app:old_template_edit", template_id=template.id)

    # お気に入り
    favorite, _ = Favorite.objects.get_or_create(user=request.user)
    favorite_items = FavoriteItem.objects.filter(favorite=favorite)

    # カテゴリ一覧
    categories = TravelCategory.objects.filter(template=template)
    for cat in categories:
        items = cat.travelitem_set.all()
        cat.total_count = items.count()
        cat.checked_count = items.filter(item_checked=TravelItem.ItemChecked.YES).count()

    # ★ 旅行全体のチェック数を追加
    all_items = TravelItem.objects.filter(travel_category__template=template)
    checked_items = all_items.filter(item_checked=TravelItem.ItemChecked.YES).count()
    total_items = all_items.count()
    
    # ★ ステータス計算を追加（← これが重要）
    today = timezone.now().date()
    if travel.end_date < today:
       status = "済"
    elif total_items > 0 and total_items == checked_items:
        status = "完"
    else:
        status = "未"

    travel.status_label = status

    context = {
        "template": template,
        "travel": travel,
        "travel_info": travel,
        "categories": categories,
        "favorite_items": favorite_items,
        "checked_items": checked_items,   # ← 追加
        "total_items": total_items,       # ← 追加
    }

    return render(request, "old_travel/template_manage.html", context)



# -------------------------------
# 項目編集（モーダル）
# -------------------------------
def edit_item(request, item_id):
    item = get_object_or_404(TravelItem, pk=item_id)

    if request.method == "POST":
        new_name = request.POST.get("item_name")

        if "delete" in request.POST:
            item.delete()
        else:
            item.item_name = new_name
            item.save()

        return redirect("app:old_template_edit", template_id=item.travel_category.template.id)

    return render(
        request,
        "old_travel/modal/edit_item_modal.html",
        {
            "item": item,
            "template_id": item.travel_category.template.id
        }
    )


# -------------------------------
# 項目追加（モーダル）
# -------------------------------
def add_item_page(request, template_id):
    if request.method == "POST":
        category_id = request.POST.get("category_id")
        category = get_object_or_404(TravelCategory, pk=category_id)

        name = request.POST.get("item_name")
        add_favorite = request.POST.get("favorite") == "1"

        TravelItem.objects.create(
            travel_category=category,
            item_name=name,
            item_checked=0
        )

        if add_favorite:
            favorite, _ = Favorite.objects.get_or_create(user=request.user)
            FavoriteItem.objects.create(
                favorite=favorite,
                item_name=name
            )

        return redirect("app:old_template_edit", template_id=template_id)

    return redirect("app:old_template_edit", template_id=template_id)


# -------------------------------
# 分類削除（個別）
# -------------------------------
def delete_category(request, category_id):
    category = get_object_or_404(TravelCategory, id=category_id)

    TravelItem.objects.filter(travel_category=category).delete()
    category.delete()
    return redirect("app:old_template_edit", template_id=category.template.id)


# -------------------------------
# 分類名編集（モーダル）
# -------------------------------
def edit_category_item(request, category_id):
    category = get_object_or_404(TravelCategory, id=category_id)

    if request.method == "POST":
        new_name = request.POST.get("category_name")
        if new_name:
            category.category_name = new_name
            category.save()

        return redirect("app:old_template_edit", template_id=category.template.id)

    return render(
        request,
        "old_travel/modal/edit_category_modal.html",
        {
            "category": category
        }
    )
def delete_template(request, template_id):
    template = get_object_or_404(Template, id=template_id)
    travel = template.travel_info

    if request.method == "POST":
        travel.delete()
        template.delete()
        return redirect("app:home")  # 一覧へ戻る

    return redirect("app:home")
