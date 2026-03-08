from django.shortcuts import render, redirect, get_object_or_404
from app.models import (
    Template, TravelCategory, TravelItem,
    Favorite, FavoriteItem
)
from app.forms.old_template_add import OldCategoryItemForm


def category_item_add(request, template_id):

    template = get_object_or_404(Template, id=template_id)
    categories = TravelCategory.objects.filter(template=template)
    color_list = TravelCategory.CategoryColor.choices

    # お気に入り
    favorite, _ = Favorite.objects.get_or_create(user=request.user)
    favorite_items = FavoriteItem.objects.filter(favorite=favorite)

    if request.method == "POST":
        form = OldCategoryItemForm(request.POST, template=template)
        continue_flag = request.POST.get("continue")

        #  エラー → エラーメッセージ表示、モーダルは出さない
        if not form.is_valid():
            return render(
                request,
                "old_travel/add_category_item.html",
                {
                    "form": form,
                    "template": template,
                    "categories": categories,
                    "color_list": color_list,
                    "favorite_items": favorite_items,
                    "open_continue_modal": False,  
                }
            )

        #  バリデーション OK
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
            TravelItem.objects.create(
                travel_category=category,
                item_name=cd["item_name"],
                item_checked=0,
            )

        #  はい → 続けて追加
        if continue_flag == "1":
            return redirect("app:category_item_add", template_id)

        #  いいえ → 戻る
        if continue_flag == "2":
            return redirect("app:old_template_edit", template_id)

        #  成功 → モーダル表示
        return render(
            request,
            "old_travel/add_category_item.html",
            {
                "form": form,
                "template": template,
                "categories": categories,
                "color_list": color_list,
                "favorite_items": favorite_items,
                "open_continue_modal": True,  # ← 成功時だけモーダルを出す
            }
        )

    # GET
    form = OldCategoryItemForm(template=template)
    return render(
        request,
        "old_travel/add_category_item.html",
        {
            "form": form,
            "template": template,
            "categories": categories,
            "color_list": color_list,
            "favorite_items": favorite_items,
        }
    )