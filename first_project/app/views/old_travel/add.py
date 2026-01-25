from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from app.models.template import Template, TravelCategory, TravelItem
from app.models.favorite import Favorite, FavoriteItem
from app.forms.template_add import CategoryItemForm


def category_item_add(request, template_id):
    template = get_object_or_404(Template, pk=template_id)

    favorite, _ = Favorite.objects.get_or_create(user=request.user)
    favorite_items = FavoriteItem.objects.filter(favorite=favorite)

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
            if item_name and favorite_flag:
                FavoriteItem.objects.get_or_create(
                    favorite=favorite,
                    item_name=item_name
                )

            return redirect(f"{request.path}?saved=1")

        # フォームエラーをメッセージ化
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, error)

        return redirect(request.path)

    # -------------------------
    # GET
    # -------------------------
    form = CategoryItemForm(template=template)
    show_continue_modal = request.GET.get("saved") == "1"

    return render(request, "old_travel/add_category_item.html", {
        "template": template,
        "favorite_items": favorite_items,
        "show_continue_modal": show_continue_modal,
        "color_list": color_list,
        "next_url": request.path,
        "form": form,
    })