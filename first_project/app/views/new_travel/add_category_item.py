from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ...models.template import Template, TravelCategory, TravelItem
from ...models.favorite import Favorite, FavoriteItem


def get_or_create_category(template, user, category_name, color):
    existing_category = TravelCategory.objects.filter(
        template=template,
        category_name=category_name
    ).first()

    if existing_category:
        if existing_category.template == template:
            return existing_category
        return TravelCategory.objects.create(
            template=template,
            category_name=category_name,
            travel_type=TravelCategory.TravelType.CUSTOM,
            category_color=color,
        )
    else:
        return TravelCategory.objects.create(
            template=template,
            category_name=category_name,
            travel_type=TravelCategory.TravelType.CUSTOM,
            category_color=color,
        )


def add_category_item(request, template_id):
    template = get_object_or_404(Template, id=template_id)
    favorite, _ = Favorite.objects.get_or_create(user=request.user)

    past_categories = (
        TravelCategory.objects
        .filter(template__user=request.user)
        .values_list("category_name", flat=True)
        .distinct()
    )

    past_items = (
        TravelItem.objects
        .filter(travel_category__template__user=request.user)
        .values_list("item_name", flat=True)
        .distinct()
    )

    favorites = favorite.items.all()
    colors = TravelCategory.CategoryColor.choices

    if request.method == "POST":
        category_name = (request.POST.get("category_name") or "").strip()
        item_name = (request.POST.get("item_name") or "").strip()
        color = request.POST.get("category_color")
        favorite_flag = request.POST.get("favorite_flag") == "1"

        # --- 必須チェック ---
        if not category_name or not item_name or not color:
            messages.error(request, "分類名・項目名・カラーは必須です。")
            return redirect("app:add_category_item", template_id=template.id)

        # --- 長さチェック ---
        if len(category_name) > 50 or len(item_name) > 50:
            messages.error(request, "分類名と項目名は50文字以内で入力してください。")
            return redirect("app:add_category_item", template_id=template.id)

        try:
            color = int(color)
        except ValueError:
            messages.error(request, "カラー選択が不正です。")
            return redirect("app:add_category_item", template_id=template.id)

        # --- カテゴリ取得 or 作成 ---
        category = get_or_create_category(template, request.user, category_name, color)

        # --- 同じカテゴリに同じ項目名が存在するかチェック ---
        if TravelItem.objects.filter(travel_category=category, item_name=item_name).exists():
            messages.error(request, "同じ分類に同じ項目がすでに存在します。")
            return redirect("app:add_category_item", template_id=template.id)

        # --- TravelItem 作成 ---
        TravelItem.objects.create(
            travel_category=category,
            item_name=item_name,
            item_checked=TravelItem.ItemChecked.NO
        )

        # --- お気に入り登録（重複チェック付き） ---
        if favorite_flag:
            FavoriteItem.objects.get_or_create(
                favorite=favorite,
                item_name=item_name
            )

        messages.success(request, "分類・項目を追加しました。")
        return redirect(f"{request.path}?saved=1")

    return render(request, "new_travel/add_category_item.html", {
        "template": template,
        "past_categories": past_categories,
        "past_items": past_items,
        "favorites": favorites,
        "colors": colors,
    })