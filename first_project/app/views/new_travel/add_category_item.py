from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ...models.template import Template, TravelCategory, TravelItem
from ...models.favorite import Favorite, FavoriteItem
from app.forms.template_add import CategoryItemForm


def add_category_item(request, template_id):
    template = get_object_or_404(Template, id=template_id)
    favorite, _ = Favorite.objects.get_or_create(user=request.user)

    # 過去カテゴリ
    past_categories = (
        TravelCategory.objects
        .filter(template__user=request.user)
        .values_list("category_name", flat=True)
        .distinct()
    )

    # お気に入り
    favorites = favorite.items.all()

    # カラーマップ
    color_map = {
        value: label[:7]
        for value, label in TravelCategory.CategoryColor.choices
    }

    # POST（登録処理）
    if request.method == "POST":
        form = CategoryItemForm(request.POST, template=template)

        if form.is_valid():
            category_name = form.cleaned_data["category_name"]
            item_name = form.cleaned_data["item_name"]
            color = form.cleaned_data["category_color"]
            favorite_flag = form.cleaned_data["favorite_flag"]

            # カテゴリ作成
            category = TravelCategory.objects.create(
                template=template,
                category_name=category_name,
                travel_type=TravelCategory.TravelType.CUSTOM,
                category_color=color,
            )

            # TravelItem 作成
            TravelItem.objects.create(
                travel_category=category,
                item_name=item_name,
                item_checked=TravelItem.ItemChecked.NO
            )

            # お気に入り登録
            if favorite_flag:
                FavoriteItem.objects.get_or_create(
                    favorite=favorite,
                    item_name=category_name,
                )

            # ⭐ POST後に再取得（最新状態でモーダル表示）
            past_categories = (
                TravelCategory.objects
                .filter(template__user=request.user)
                .values_list("category_name", flat=True)
                .distinct()
            )
            favorites = favorite.items.all()

            # ⭐ リダイレクトしない → モーダルを表示できる
            return render(request, "new_travel/add_category_item.html", {
                "template": template,
                "past_categories": past_categories,
                "favorite_items": favorites,
                "color_map": color_map,
                "form": CategoryItemForm(template=template),  # 空フォーム
                "show_continue_modal": True,  # ← モーダル表示フラグ
            })

        else:
            # フォームエラー
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

            return redirect("app:add_category_item", template_id=template.id)

    # GET（初期表示）
    else:
        form = CategoryItemForm(template=template)

    return render(request, "new_travel/add_category_item.html", {
        "template": template,
        "past_categories": past_categories,
        "favorite_items": favorites,
        "color_map": color_map,
        "form": form,
    })