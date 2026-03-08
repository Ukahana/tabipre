from django.shortcuts import render, get_object_or_404, redirect
from ...models.template import Template, TravelCategory, TravelItem
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

def template_edit2(request, template_id):
    template = get_object_or_404(Template, id=template_id)

    if request.method == "POST":

        print("=== template_edit2 POST ===")
        print(request.POST)

        # --- ① まず全ての編集内容を保存する ---
        for category in template.travelcategory_set.all():
            for item in category.travelitem_set.all():

                # チェック状態
                checked = request.POST.get(f"item_checked_{item.id}") == "on"
                item.item_checked = checked

                # 名前変更
                new_name = request.POST.get(f"rename_{item.id}")
                if new_name is not None:
                    item.item_name = new_name

                item.save()

        # --- ② 分類追加ボタン ---
        if "go_add" in request.POST:
            return redirect("app:add_category_item", template_id=template.id)

        # --- ③ 削除処理 ---
        delete_cat_id = request.POST.get("delete_category")
        if delete_cat_id and delete_cat_id.isdigit():
            TravelCategory.objects.filter(id=delete_cat_id).delete()
            return redirect("app:template_edit2", template_id=template.id)

        delete_item_id = request.POST.get("delete_item")
        if delete_item_id and delete_item_id.isdigit():
            TravelItem.objects.filter(id=delete_item_id).delete()
            return redirect("app:template_edit2", template_id=template.id)

        # --- ④ 保存ボタン ---
        if "save_changes" in request.POST:
            return redirect("app:home")

        return redirect("app:template_edit2", template_id=template.id)

    # GET
    categories = TravelCategory.objects.filter(template=template).order_by("id")

    return render(request, "new_travel/template_edit2.html", {
        "template": template,
        "categories": categories,
    })