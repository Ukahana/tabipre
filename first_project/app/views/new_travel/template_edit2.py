from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ...models.template import Template, TravelCategory, TravelItem

def template_edit2(request, template_id):
    template = get_object_or_404(Template, id=template_id)

    if request.method == "POST":

        # --- 分類削除処理 ---
        delete_cat_id = request.POST.get("delete_category")
        if delete_cat_id:
           TravelItem.objects.filter(travel_category_id=delete_cat_id).delete()
           TravelCategory.objects.filter(id=delete_cat_id).delete()

           return redirect("app:template_edit2", template_id=template.id)

        # --- 項目削除処理 ---
        delete_id = request.POST.get("delete_item")
        if delete_id:
            TravelItem.objects.filter(id=delete_id).delete()
            return redirect("app:template_edit2", template_id=template.id)


        # --- アイテム更新 ---
        for item in TravelItem.objects.filter(travel_category__template=template):

            # チェック状態
            checked = request.POST.get(f"item_checked_{item.id}")
            item.item_checked = 1 if checked else 0

            # 名前変更
            new_name = request.POST.get(f"rename_{item.id}")
            if new_name:
                item.item_name = new_name

            # カテゴリ変更
            new_cat_id = request.POST.get(f"category_{item.id}")
            if new_cat_id:
                item.travel_category_id = new_cat_id

            item.save()

        return redirect("app:home")  # ← 保存時はホームへ

    # GET
    categories = TravelCategory.objects.filter(template=template)

    for cat in categories:
        cat.checked_count = cat.travelitem_set.filter(item_checked=1).count()
        cat.total_count = cat.travelitem_set.count()

    return render(request, "new_travel/template_edit2.html", {
        "template": template,
        "categories": categories,
    })