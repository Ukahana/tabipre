from django.shortcuts import render, redirect, get_object_or_404
from app.models import (
    Template, TravelCategory, TravelItem,
    Favorite, FavoriteItem
)
from app.forms.template_add import CategoryItemForm


def add_category_item(request, template_id):

    template = get_object_or_404(Template, id=template_id)

    # 過去の分類名（datalist 用）
    past_categories = TravelCategory.objects.filter(
        template=template
    ).values_list("category_name", flat=True)

    # お気に入り
    favorite, _ = Favorite.objects.get_or_create(user=request.user)
    favorite_items = FavoriteItem.objects.filter(favorite=favorite)

    # カラー一覧
    color_map = dict(TravelCategory.CategoryColor.choices)

    # ============================
    # POST
    # ============================
    if request.method == "POST":
        form = CategoryItemForm(request.POST, template=template)
        continue_flag = request.POST.get("continue")

        # ★ バリデーション NG → エラー表示（モーダル出さない）
        if not form.is_valid():
            return render(
                request,
                "new_travel/add_category_item.html",
                {
                    "form": form,
                    "template": template,
                    "past_categories": past_categories,
                    "favorite_items": favorite_items,
                    "color_map": color_map,
                    "open_continue_modal": False,
                }
            )

        # ★ バリデーション OK
        cd = form.cleaned_data

        # 分類を取得 or 作成
        category, _ = TravelCategory.objects.get_or_create(
            template=template,
            category_name=cd["category_name"],
            defaults={
                "category_color": cd["category_color"],
                "travel_type": TravelCategory.TravelType.CUSTOM,
            }
        )

        # 項目名があれば TravelItem を作成
        if cd["item_name"]:
            item = TravelItem.objects.create(
                travel_category=category,
                item_name=cd["item_name"],
                item_checked=0,
            )

            # ★ お気に入り登録（重複チェック付き）
            if cd["favorite_flag"] == 1:
                if not FavoriteItem.objects.filter(
                    favorite=favorite,
                    item_name=item.item_name
                ).exists():
                    FavoriteItem.objects.create(
                        favorite=favorite,
                        item_name=item.item_name
                    )

        # ★ はい → 続けて追加（保存済み）
        if continue_flag == "1":
            return redirect("app:add_category_item", template_id)

        # ★ いいえ → 戻る（保存済み）
        if continue_flag == "2":
            return redirect("app:template_edit2", template_id)

        # ★ モーダル表示（保存済み）
        return render(
            request,
            "new_travel/add_category_item.html",
            {
                "form": CategoryItemForm(template=template),  # 空フォーム
                "template": template,
                "past_categories": past_categories,
                "favorite_items": favorite_items,
                "color_map": color_map,
                "open_continue_modal": True,
            }
        )

    # ============================
    # GET
    # ============================
    hidden = request.session.get("edit_hidden")
    
    form = CategoryItemForm(template=template)
    return render(
        request,
        "new_travel/add_category_item.html",
        {
            "form": form,
            "template": template,
            "past_categories": past_categories,
            "favorite_items": favorite_items,
            "color_map": color_map,
            "is_share_edit": False,
            "hidden": hidden,
        }
    )