from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from app.models import TravelCategory, TravelItem, Template, Favorite, FavoriteItem
from app.forms.old_template_add import OldCategoryItemForm

def category_item_add(request, template_id):

    template = get_object_or_404(Template, id=template_id)

    categories = TravelCategory.objects.filter(template_id=template_id)
    color_list = [
        {"value": 0, "code": "#e91e63ff"},
        {"value": 1, "code": "#ffb7b2fe"},
        {"value": 2, "code": "#f57c00ff"},
        {"value": 3, "code": "#388e3cff"},
        {"value": 4, "code": "#0097a7ff"},
        {"value": 5, "code": "#303f9ffe"},
        {"value": 6, "code": "#795548ff"},
        {"value": 7, "code": "#7b1fa2ff"},
    ]

    # ★ お気に入りリストを取得
    favorite, created = Favorite.objects.get_or_create(user=request.user)
    favorite_items = favorite.items.all()

    if request.method == "POST":
        form = OldCategoryItemForm(request.POST)

        if not form.is_valid():
            return render(request, "old_travel/add_category_item.html", {
                "template": template,
                "categories": categories,
                "color_list": color_list,
                "form": form,
                "favorite_items": favorite_items,
            })

        # 正常処理
        category_name = form.cleaned_data["category_name"]
        category_color = form.cleaned_data["category_color"]
        item_name = form.cleaned_data["item_name"]
        favorite_flag = form.cleaned_data["favorite_flag"]

        category, created = TravelCategory.objects.get_or_create(
            template=template,
            category_name=category_name,
            defaults={
                "category_color": category_color,
                "travel_type": TravelCategory.TravelType.CUSTOM,
            }
        )

        if not created and category.category_color != category_color:
            category.category_color = category_color
            category.save()

        # TravelItem を作成
        TravelItem.objects.create(
            travel_category=category,
            item_name=item_name or "",
            item_checked=1 if favorite_flag == 1 else 0
        )

        # ★ FavoriteItem にも保存（これが必要）
        if favorite_flag == 1:
            FavoriteItem.objects.create(
                favorite=favorite,
                item_name=item_name
            )

        return redirect(f"{request.path}?success=1")

    # GET のとき
    form = OldCategoryItemForm()

    return render(request, "old_travel/add_category_item.html", {
        "template": template,
        "categories": categories,
        "color_list": color_list,
        "form": form,
        "favorite_items": favorite_items,
    })