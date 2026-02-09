from django.shortcuts import render, get_object_or_404, redirect
from ...models.template import Template, TravelCategory, TravelItem
from ...models.favorite import Favorite, FavoriteItem
from app.forms.template_add import CategoryItemForm


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
        request.session["edit_hidden"] = request.POST
        form = CategoryItemForm(request.POST, template=template)

        if form.is_valid():
            category_name = form.cleaned_data["category_name"]
            item_name = form.cleaned_data["item_name"]
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

            return redirect("app:template_edit2", template_id=template.id)

        # エラー時はそのまま返す
        return render(request, "new_travel/add_category_item.html", {
            "template": template,
            "past_categories": past_categories,
            "favorite_items": favorites,
            "color_map": color_map,
            "form": form,
        })

    # GET
    form = CategoryItemForm(template=template)

    return render(request, "new_travel/add_category_item.html", {
        "template": template,
        "past_categories": past_categories,
        "favorite_items": favorites,
        "color_map": color_map,
        "form": form,
    })