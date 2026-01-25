from django.shortcuts import render, get_object_or_404, redirect
from ...models.template import Template, TravelCategory, TravelItem

def template_edit2(request, template_id):
    template = get_object_or_404(Template, id=template_id)

    if request.method == "POST":

        # --- 分類削除 ---
        delete_cat_id = request.POST.get("delete_category")
        if delete_cat_id and delete_cat_id.isdigit():
            TravelCategory.objects.filter(id=delete_cat_id).delete()
            return redirect("app:template_edit2", template_id=template.id)


        # --- 項目削除 ---
        delete_item_id = request.POST.get("delete_item")
        if delete_item_id and delete_item_id.isdigit():
           TravelItem.objects.filter(id=delete_item_id).delete()
           return redirect("app:template_edit2", template_id=template.id)

        # --- アイテム更新 ---
        for item in TravelItem.objects.filter(travel_category__template=template):

            # チェック更新
            checked = request.POST.get(f"item_checked_{item.id}")
            item.item_checked = 1 if checked else 0

            # 名前更新
            new_name = request.POST.get(f"rename_{item.id}")
            if new_name:
                item.item_name = new_name

            item.save()

        # 保存後も同じ画面に戻る
        return redirect("app:template_edit2", template_id=template.id)

    # GET
    categories = TravelCategory.objects.filter(template=template).order_by("id")

    for cat in categories:
        cat.checked_count = cat.travelitem_set.filter(item_checked=1).count()
        cat.total_count = cat.travelitem_set.count()

    return render(request, "new_travel/template_edit2.html", {
        "template": template,
        "categories": categories,
    })