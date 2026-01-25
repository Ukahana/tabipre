from django.shortcuts import render, get_object_or_404, redirect
from ...models.template import Template, TravelCategory, TravelItem

def old_template_copy(request, template_id):
    template = get_object_or_404(Template, id=template_id)

    if request.method == "POST":

        # --- メモ更新 ---
        new_memo = request.POST.get("memo")
        if new_memo is not None:
            template.travel_info.memo = new_memo
            template.travel_info.save()

        # --- 分類削除 ---
        delete_cat_id = request.POST.get("delete_category")
        if delete_cat_id and delete_cat_id.isdigit():
            TravelItem.objects.filter(travel_category_id=delete_cat_id).delete()
            TravelCategory.objects.filter(id=delete_cat_id).delete()
            return redirect("app:old_template_edit", template_id=template.id)

        # --- 項目削除 ---
        delete_id = request.POST.get("delete_item")
        if delete_id and delete_id.isdigit():
            TravelItem.objects.filter(id=delete_id).delete()
            return redirect("app:old_template_edit", template_id=template.id)

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

        # ★ 保存後はホーム画面へ遷移
        return redirect("app:home")

    # --- GET ---
    categories = TravelCategory.objects.filter(template=template)

    return render(request, "new_travel/old_template.html", {
        "template": template,
        "categories": categories,
    })