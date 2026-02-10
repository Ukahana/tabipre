from django.shortcuts import render, redirect, get_object_or_404
from ...models.template import Template, TravelCategory, TravelItem
from ...models.favorite import Favorite, FavoriteItem
from ...forms.template_add import CategoryItemForm


def add_category_item(request, template_id):
    template = get_object_or_404(Template, id=template_id)

    past_categories = TravelCategory.objects.filter(template=template).values_list("category_name", flat=True)
    favorite_list = Favorite.objects.get(user=request.user)
    favorite_items = favorite_list.items.all()
    color_map = dict(TravelCategory.CategoryColor.choices)

    if request.method == "POST":
        continue_flag = request.POST.get("continue", "0")
        form = CategoryItemForm(request.POST, template=template)

        # ★ いいえ（continue=2）→ edit2 に戻る
        if continue_flag == "2":
            return redirect("app:template_edit2", template_id=template.id)

        # ① 最初の登録（continue=0）
        if continue_flag == "0":
            if form.is_valid():
                # モーダルを出す
                return render(request, "new_travel/add_category_item.html", {
                    "template": template,
                    "past_categories": past_categories,
                    "favorite_items": favorite_items,
                    "color_map": color_map,
                    "form": form,
                    "open_continue_modal": True,
                })
            else:
                # エラー表示
                return render(request, "new_travel/add_category_item.html", {
                    "template": template,
                    "past_categories": past_categories,
                    "favorite_items": favorite_items,
                    "color_map": color_map,
                    "form": form,
                    "open_continue_modal": False,
                })

        # ② モーダルの「はい」（continue=1）
        if continue_flag == "1":
            if form.is_valid():
                category_name = form.cleaned_data["category_name"]
                item_name = form.cleaned_data["item_name"]
                category_color = form.cleaned_data["category_color"]

                # 分類取得 or 作成
                category, created = TravelCategory.objects.get_or_create(
                    template=template,
                    category_name=category_name,
                    defaults={
                        "category_color": category_color,
                        "travel_type": TravelCategory.TravelType.CUSTOM,
                    }
                )

                # ★ 重複チェック（同じ分類内に同じ項目名があるか）
                if item_name:
                    if TravelItem.objects.filter(
                        travel_category=category,
                        item_name=item_name
                    ).exists():
                        form.add_error("item_name", "この分類には同じ項目がすでに存在します。")
                        return render(request, "new_travel/add_category_item.html", {
                            "template": template,
                            "past_categories": past_categories,
                            "favorite_items": favorite_items,
                            "color_map": color_map,
                            "form": form,
                            "open_continue_modal": False,
                        })

                # 色変更
                if not created and category.category_color != category_color:
                    category.category_color = category_color
                    category.save()

                # 項目追加
                if item_name:
                    TravelItem.objects.create(
                        travel_category=category,
                        item_name=item_name,
                        item_checked=0,
                    )

                # 保存後は空フォーム
                empty_form = CategoryItemForm(template=template)
                return render(request, "new_travel/add_category_item.html", {
                    "template": template,
                    "past_categories": past_categories,
                    "favorite_items": favorite_items,
                    "color_map": color_map,
                    "form": empty_form,
                    "open_continue_modal": False,
                })

            # バリデーションNG（ほぼ起きない）
            return render(request, "new_travel/add_category_item.html", {
                "template": template,
                "past_categories": past_categories,
                "favorite_items": favorite_items,
                "color_map": color_map,
                "form": form,
                "open_continue_modal": False,
            })

    # GET
    form = CategoryItemForm(template=template)
    return render(request, "new_travel/add_category_item.html", {
        "template": template,
        "past_categories": past_categories,
        "favorite_items": favorite_items,
        "color_map": color_map,
        "form": form,
        "open_continue_modal": False,
    })