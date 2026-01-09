from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ...models.travel import Travel_info
from ...models.template import Template, TravelCategory, TravelItem
from ...models.favorite import Favorite, FavoriteItem

# -------------------------------
# テンプレート編集（travel_edit2）
# -------------------------------
def old_template_editor(request, template_id):
    template = get_object_or_404(Template, id=template_id)
    travel = template.travel_info

    favorite, created = Favorite.objects.get_or_create(user=request.user)
    favorite_items = FavoriteItem.objects.filter(favorite=favorite)

    categories = TravelCategory.objects.filter(template=template)

    for cat in categories:
        cat.checked_count = cat.travelitem_set.filter(item_checked=1).count()
        cat.total_count = cat.travelitem_set.count()

    context = {
        "template": template,
        "travel": travel,
        "categories": categories,
        "favorite_items": favorite_items,
    }

    return render(request, "old_travel/template_editor.html", context)
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

        return redirect("app:template_editor", template_id=item.travel_category.template.id)

    return render(request, "old_travel/modal/edit_item_modal.html", {"item": item})

# -------------------------------
# 項目追加（モーダル）
# -------------------------------
def add_item(request, category_id):
    category = get_object_or_404(TravelCategory, pk=category_id)

    if request.method == "POST":
        name = request.POST.get("item_name")
        add_favorite = request.POST.get("favorite") == "on"

        TravelItem.objects.create(
            travel_category=category,
            item_name=name,
            item_checked=0
        )

        if add_favorite:
            favorite, created = Favorite.objects.get_or_create(user=request.user)
            FavoriteItem.objects.create(
                favorite=favorite,
                item_name=name
            )

        return redirect("app:template_editor", template_id=category.template.id)

    return render(request, "tabipre/modal/add_item_modal.html", {"category": category})


def delete_category(request, category_id):
    category = get_object_or_404(TravelCategory, id=category_id)

    TravelItem.objects.filter(travel_category=category).delete()
    category.delete()
    return redirect("app:template_editor", template_id=category.template.id)

def template_editor(request, template_id):
    template = get_object_or_404(Template, id=template_id)
    travel = template.travel_info
    # ★★★ 分類削除（POST）★★★
    if request.method == "POST":
        delete_cat_id = request.POST.get("delete_category")
        if delete_cat_id:
            category = get_object_or_404(TravelCategory, id=delete_cat_id)

            # 項目 → 分類の順で削除
            TravelItem.objects.filter(travel_category=category).delete()
            category.delete()

            return redirect("app:template_editor", template_id=template.id)


    # --- ステータス判定（①） ---
    today = timezone.now().date()
    if travel.end_date < today:
        travel.status_label = "済"
    else:
        items = TravelItem.objects.filter(
            travel_category__template__travel_info=travel
        )
        total = items.count()
        done = items.filter(item_checked=TravelItem.ItemChecked.YES).count()
        travel.status_label = "完" if total > 0 and total == done else "未"

    # --- カテゴリ一覧（②） ---
    categories = TravelCategory.objects.filter(template=template)
    for cat in categories:
        items = cat.travelitem_set.all()
        cat.total_count = items.count()
        cat.checked_count = items.filter(item_checked=TravelItem.ItemChecked.YES).count()

    return render(request, "new_travel/template_editor.html", {
        "template": template,
        "travel": travel,
        "categories": categories,
    })

def edit_category_item(request, category_id):
    category = get_object_or_404(TravelCategory, id=category_id)

    if request.method == "POST":
        new_name = request.POST.get("category_name")
        if new_name:
            category.category_name = new_name
            category.save()

        return redirect("app:template_editor", template_id=category.template.id)

    return render(request, "old_travel/modal/edit_category_modal.html", {
        "category": category
    })