from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from app.models.template import Template, TravelCategory, TravelItem
from app.models.favorite import Favorite, FavoriteItem


def get_or_create_category(template, user, category_name, color):
    existing_category = TravelCategory.objects.filter(
        template=template,
        category_name=category_name
    ).first()

    if existing_category:
        return existing_category

    return TravelCategory.objects.create(
        template=template,
        category_name=category_name,
        travel_type=TravelCategory.TravelType.CUSTOM,
        category_color=color,
    )


def category_item_add(request, template_id):
    template = get_object_or_404(Template, pk=template_id)

    # お気に入りリスト
    favorite, _ = Favorite.objects.get_or_create(user=request.user)
    favorite_items = FavoriteItem.objects.filter(favorite=favorite)

    # ★ カラーパレット用
    color_map = {
        0: "#e91e63ff",
        1: "#ffb7b2fe",
        2: "#f57c00ff",
        3: "#388e3cff",
        4: "#0097a7ff",
        5: "#303f9ffe",
        6: "#795548ff",
        7: "#7b1fa2ff",
    }

    color_list = [
        {"value": value, "code": color_map[value]}
        for value, _ in TravelCategory.CategoryColor.choices
    ]

    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        category_name = (request.POST.get("category_name") or "").strip()
        item_name = (request.POST.get("item_name") or "").strip()
        color = request.POST.get("category_color")

        if not category_name or not color:
            messages.error(request, "分類名とカラーは必須です。")
            return redirect(request.path)

        if len(category_name) > 50:
            messages.error(request, "分類名は50文字以内で入力してください。")
            return redirect(request.path)

        if item_name and len(item_name) > 50:
            messages.error(request, "項目名は50文字以内で入力してください。")
            return redirect(request.path)

        try:
            color = int(color)
        except ValueError:
            messages.error(request, "カラー選択が不正です。")
            return redirect(request.path)

        category = get_or_create_category(template, request.user, category_name, color)

        if item_name:
            if TravelItem.objects.filter(travel_category=category, item_name=item_name).exists():
                messages.error(request, "同じ分類に同じ項目がすでに存在します。")
                return redirect(request.path)

        TravelItem.objects.create(
            travel_category=category,
            item_name=item_name,
            item_checked=TravelItem.ItemChecked.NO
        )

        if item_name and request.POST.get("favorite_flag") == "1":
            FavoriteItem.objects.get_or_create(
                favorite=favorite,
                item_name=item_name
            )

        return redirect(f"{request.path}?saved=1")

    # -------------------------
    # GET（ここが POST の外に必要）
    # -------------------------
    show_continue_modal = request.GET.get("saved") == "1"

    return render(request, "old_travel/add_category_item.html", {
        "template": template,
        "favorite_items": favorite_items,
        "show_continue_modal": show_continue_modal,
        "color_list": color_list,
    })