from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ...models.template import Template, TravelCategory, TravelItem

def template_edit2(request, template_id):
    template = get_object_or_404(Template, id=template_id)

    if request.method == "POST":

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

        # --- 削除処理 ---
        delete_id = request.POST.get("delete_item")
        if delete_id:
            TravelItem.objects.filter(id=delete_id).delete()

        messages.success(request, "テンプレートを更新しました")
        return redirect("app:template_edit", template_id=template_id)

    # GET
    categories = TravelCategory.objects.filter(template=template)

    return render(request, "new_travel/template_edit.html", {
        "template": template,
        "categories": categories,
    })