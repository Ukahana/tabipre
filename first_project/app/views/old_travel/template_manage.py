from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ...models.template import Template, TravelCategory, TravelItem
from ...models.favorite import Favorite, FavoriteItem
from django.contrib import messages


# -------------------------------
# テンプレート編集（old_template_edit）
# -------------------------------
def old_template_edit(request, template_id):
    template = get_object_or_404(Template, id=template_id)
    travel = template.travel_info

    if request.method == "POST":

        # テンプレート削除
        delete_template_id = request.POST.get("delete_template")
        if delete_template_id:
            template = get_object_or_404(Template, id=delete_template_id)
            travel = template.travel_info
            template.delete()
            travel.delete()
            return redirect("app:home")

        # 分類削除
        delete_cat_id = request.POST.get("delete_category")
        if delete_cat_id:
            category = get_object_or_404(
                TravelCategory,
                id=delete_cat_id,
                template=template
            )
            TravelItem.objects.filter(travel_category=category).delete()
            category.delete()
            return redirect("app:old_template_edit", template_id=template.id)

        # 項目削除
        delete_item_id = request.POST.get("delete_item_id")
        if delete_item_id:
            item = get_object_or_404(TravelItem, id=delete_item_id)
            template_id = item.travel_category.template.id
            item.delete()
            return redirect("app:old_template_edit", template_id=template_id)

    favorite, _ = Favorite.objects.get_or_create(user=request.user)
    favorite_items = FavoriteItem.objects.filter(favorite=favorite)

    categories = TravelCategory.objects.filter(template=template)
    for cat in categories:
        cat.total_count_display = cat.total_count
        cat.checked_count_display = cat.checked_count

    all_items = TravelItem.objects.filter(travel_category__template=template)
    checked_items = all_items.filter(item_checked=TravelItem.ItemChecked.YES).count()
    total_items = all_items.count()

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
        "current_template": template,
        "travel": travel,
        "travel_info": travel,
        "categories": categories,
        "favorite_items": favorite_items,
        "checked_items": checked_items,
        "total_items": total_items,
        "card_travel_info": template.travel_info,
        "open_edit_modal": request.session.pop("open_edit_modal", None),
        "edit_item_name": request.session.pop("edit_item_name", ""),
        "add_item_error": request.session.pop("add_item_error", False),
        "old_value": request.session.pop("old_value", ""),
        "error_category_id": request.session.pop("error_category_id", None),
    }

    return render(request, "old_travel/template_manage.html", context)



# -------------------------------
# 項目編集（モーダル）
# -------------------------------
def edit_item(request, item_id=None):
    if request.method == "POST":

        # 削除モーダルからの削除
        delete_item_id = request.POST.get("delete_item_id")
        if delete_item_id:
            item = get_object_or_404(TravelItem, id=delete_item_id)
            item.delete()
            return redirect("app:old_template_edit", template_id=item.travel_category.template.id)

        # 編集モーダルの更新・削除
        post_item_id = request.POST.get("edit_item_id")
        item = get_object_or_404(TravelItem, pk=post_item_id)

        # 編集モーダルの削除
        if request.POST.get("delete_item") == "1":
            item.delete()
            return redirect("app:old_template_edit", template_id=item.travel_category.template.id)

        new_name = request.POST.get("item_name", "").strip()

        # 必須チェック
        if not new_name:
            messages.error(request, "項目名を入力してください。")
            request.session["open_edit_modal"] = item.id
            request.session["edit_item_name"] = new_name
            return redirect("app:old_template_edit", template_id=item.travel_category.template.id)

        # 文字数チェック
        if len(new_name) > 50:
            messages.error(request, "項目名は50文字以内で入力してください。")
            request.session["open_edit_modal"] = item.id
            request.session["edit_item_name"] = new_name
            return redirect("app:old_template_edit", template_id=item.travel_category.template.id)

        # 重複チェック
        if TravelItem.objects.filter(
            travel_category=item.travel_category,
            item_name=new_name
        ).exclude(id=item.id).exists():
            messages.error(request, "同じ名前の項目がすでに存在します。")
            request.session["open_edit_modal"] = item.id
            request.session["edit_item_name"] = new_name
            return redirect("app:old_template_edit", template_id=item.travel_category.template.id)

        # 更新処理
        item.item_name = new_name
        item.save()

        return redirect("app:old_template_edit", template_id=item.travel_category.template.id)

    return redirect("app:home")
# -------------------------------
# 項目追加（モーダル）
# -------------------------------
def add_item_page(request, template_id):
    template = get_object_or_404(Template, id=template_id)

    if request.method == "POST":
        category_id = request.POST.get("category_id")
        name = request.POST.get("item_name", "").strip()
        add_favorite = request.POST.get("favorite") == "1"

        # --- 分類取得（エラー対策） ---
        try:
            category = TravelCategory.objects.get(pk=category_id, template=template)
        except (TravelCategory.DoesNotExist, ValueError, TypeError):
            messages.error(request, "項目を追加できませんでした。もう一度お試しください。")
            request.session["add_item_error"] = True
            request.session["old_value"] = name
            request.session["error_category_id"] = category_id
            return redirect("app:old_template_edit", template_id=template_id)

        # --- バリデーション ---
        if not name:
            messages.error(request, "項目名を入力してください。")
            request.session["add_item_error"] = True
            request.session["old_value"] = name
            request.session["error_category_id"] = category_id
            return redirect("app:old_template_edit", template_id=template_id)

        if len(name) > 50:
            messages.error(request, "項目名は50文字以内で入力してください。")
            request.session["add_item_error"] = True
            request.session["old_value"] = name
            request.session["error_category_id"] = category_id
            return redirect("app:old_template_edit", template_id=template_id)

        # --- 分類内で重複チェック ---
        if TravelItem.objects.filter(travel_category=category, item_name=name).exists():
            messages.error(request, "同じ分類内に同じ名前の項目があります。")
            request.session["add_item_error"] = True
            request.session["old_value"] = name
            request.session["error_category_id"] = category_id
            return redirect("app:old_template_edit", template_id=template_id)

        TravelItem.objects.create(
            travel_category=category,
            item_name=name,
            item_checked=0
        )

        # --- お気に入り登録---
        if add_favorite:
            favorite, _ = Favorite.objects.get_or_create(user=request.user)

            # すでに存在する場合は登録しない
            if not FavoriteItem.objects.filter(favorite=favorite, item_name=name).exists():
                FavoriteItem.objects.create(favorite=favorite, item_name=name)

        return redirect("app:old_template_edit", template_id=template_id)

    return redirect("app:old_template_edit", template_id=template_id)


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
