from django.shortcuts import render, get_object_or_404, redirect
from app.models.template import Template, TravelCategory, TravelItem
from app.models.favorite import Favorite, FavoriteItem
from app.forms.old_template_add import OldCategoryItemForm


def category_item_add(request, template_id):
    template = get_object_or_404(Template, id=template_id)
    favorite, _ = Favorite.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = OldCategoryItemForm(request.POST)

        if form.is_valid():
            category_name = form.cleaned_data["category_name"]
            item_name = form.cleaned_data["item_name"]
            color = form.cleaned_data["category_color"]
            favorite_flag = form.cleaned_data["favorite_flag"]

            # ⭐ 既存分類があるかチェック
            existing_category = TravelCategory.objects.filter(
                template=template,
                category_name=category_name
            ).first()

            if existing_category:
                category = existing_category
            else:
                category = TravelCategory.objects.create(
                    template=template,
                    category_name=category_name,
                    travel_type=TravelCategory.TravelType.CUSTOM,
                    category_color=color,
                )

            # ⭐ 項目追加
            TravelItem.objects.create(
                travel_category=category,
                item_name=item_name or "",
                item_checked=TravelItem.ItemChecked.NO
            )

            # ⭐ お気に入り登録
            if item_name and favorite_flag:
                FavoriteItem.objects.get_or_create(
                    favorite=favorite,
                    item_name=item_name
                )

            # ⭐ ボタン判定
            action = request.POST.get("action")

            if action == "continue":
                return redirect("app:category_item_add", template_id=template.id)
            else:
                return redirect("app:old_template_edit", template_id=template.id)

    else:
        form = OldCategoryItemForm()

    categories = TravelCategory.objects.filter(template=template)

    # ⭐ 色パレットをテンプレートが期待する形に整形
    raw_colors = TravelCategory.CategoryColor.choices
    color_list = [{"value": v, "code": code} for v, code in raw_colors]

    # ⭐ お気に入り一覧
    favorite_items = FavoriteItem.objects.filter(favorite=favorite)

    return render(request, "old_travel/add_category_item.html", {
        "form": form,
        "template": template,
        "categories": categories,
        "color_list": color_list,
        "favorite_items": favorite_items,
    })