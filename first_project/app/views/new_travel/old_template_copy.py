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
            return redirect(request.path)

        # --- 項目削除 ---
        delete_id = request.POST.get("delete_item")
        if delete_id and delete_id.isdigit():
            TravelItem.objects.filter(id=delete_id).delete()
            return redirect(request.path)

        # --- 名前編集 ---
        edit_item_id = request.POST.get("edit_item_id")
        if edit_item_id and edit_item_id.isdigit():
            item = TravelItem.objects.get(id=edit_item_id)
            new_name = request.POST.get("item_name")
            if new_name:
                item.item_name = new_name
                item.save()
            return redirect(request.path)

        # --- チェック更新 ---
        for item in TravelItem.objects.filter(travel_category__template=template):
            checked = request.POST.get(f"item_checked_{item.id}")
            item.item_checked = 1 if checked else 0
            item.save()

        # ★ 保存ボタン → home（最後に判定）
        if "save_changes" in request.POST:
            return redirect("app:home")

        # その他の POST は同じ画面へ
        return redirect(request.path)

    # GET
    categories = TravelCategory.objects.filter(template=template)
    return render(request, "new_travel/old_template.html", {
        "template": template,
        "categories": categories,
    })