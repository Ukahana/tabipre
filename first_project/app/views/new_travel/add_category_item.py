from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ...models.template import Template, TravelCategory, TravelItem
from ...models.favorite import Favorite, FavoriteItem
from app.forms.template_add import CategoryItemForm
import unicodedata


# 入力を正規化（全角→半角、前後の空白除去）
def normalize(text):
    if not text:
        return ""
    return unicodedata.normalize("NFKC", text).strip()


def add_category_item(request, template_id):
    template = get_object_or_404(Template, id=template_id)
    favorite, _ = Favorite.objects.get_or_create(user=request.user)

    past_categories = (
        TravelCategory.objects
        .filter(template__user=request.user)
        .values_list("category_name", flat=True)
        .distinct()
    )
    favorites = favorite.items.all()

    color_map = {
        value: label[:7]
        for value, label in TravelCategory.CategoryColor.choices
    }

    if request.method == "POST":
        print("=== add_category_item POST ===")
        print(request.POST)

        # ⭐ edit2 の hidden を維持
        request.session["edit_hidden"] = request.POST

        form = CategoryItemForm(request.POST, template=template)

        if form.is_valid():
            category_name = normalize(form.cleaned_data["category_name"])
            item_name = normalize(form.cleaned_data["item_name"])
            color = form.cleaned_data["category_color"]
            favorite_flag = form.cleaned_data["favorite_flag"]

            category, created = TravelCategory.objects.get_or_create(
                template=template,
                category_name=category_name,
                defaults={
                    "travel_type": TravelCategory.TravelType.CUSTOM,
                    "category_color": color,
                }
            )

            TravelItem.objects.create(
                travel_category=category,
                item_name=item_name or "",
                item_checked=TravelItem.ItemChecked.NO
            )

            if item_name and favorite_flag:
                FavoriteItem.objects.get_or_create(
                    favorite=favorite,
                    item_name=item_name,
                )

            if "continue" in request.POST:
                return redirect("app:add_category_item", template_id=template.id)
            else:
                return redirect("app:template_edit2", template_id=template.id)

        return redirect("app:add_category_item", template_id=template.id)

    form = CategoryItemForm(template=template)

    return render(request, "new_travel/add_category_item.html", {
        "template": template,
        "past_categories": past_categories,
        "favorite_items": favorites,
        "color_map": color_map,
        "form": form,
    })