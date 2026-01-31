from django.shortcuts import render, get_object_or_404, redirect
from ...models.template import Template, TravelCategory, TravelItem

def template_edit2(request, template_id):
    template = get_object_or_404(Template, id=template_id)

    # ⭐ hidden input の内容（セッションから取得）
    hidden = request.session.get("edit_hidden")

    # -------------------------
    # POST（保存・削除・更新・分類追加）
    # -------------------------
    if request.method == "POST":

        print("=== template_edit2 POST ===")
        print(request.POST)

        # ⭐ 分類追加ボタン
        if "go_add" in request.POST:

            # POST をコピー
            data = request.POST.copy()

            # rename の値で hidden_name を上書きする
            for key, value in request.POST.items():
                if key.startswith("rename_"):
                    item_id = key.replace("rename_", "")
                    hidden_key = f"hidden_name_{item_id}"
                    data[hidden_key] = value  # 上書き

            # hidden をセッションに保存
            request.session["edit_hidden"] = data

            return redirect("app:add_category_item", template_id=template.id)

        # --- ① まずアイテム更新（rename / checked） ---
        for item in TravelItem.objects.filter(travel_category__template=template):

            checked = request.POST.get(f"item_checked_{item.id}")
            item.item_checked = 1 if checked else 0

            new_name = request.POST.get(f"rename_{item.id}")
            if new_name:
                item.item_name = new_name

            item.save()

        # --- ② その後で削除処理 ---
        delete_cat_id = request.POST.get("delete_category")
        if delete_cat_id and delete_cat_id.isdigit():
            TravelCategory.objects.filter(id=delete_cat_id).delete()
            return redirect("app:template_edit2", template_id=template.id)

        delete_item_id = request.POST.get("delete_item")
        if delete_item_id and delete_item_id.isdigit():
            TravelItem.objects.filter(id=delete_item_id).delete()
            return redirect("app:template_edit2", template_id=template.id)

        # ⭐ 保存ボタン
        if "save_changes" in request.POST:
            if "edit_hidden" in request.session:
                del request.session["edit_hidden"]
            return redirect("app:home")

        return redirect("app:template_edit2", template_id=template.id)

    # -------------------------
    # GET（画面表示）
    # -------------------------
    categories = TravelCategory.objects.filter(template=template).order_by("id")

    # ⭐⭐⭐ GET のときに hidden を復元する（ここが最重要） ⭐⭐⭐
    if hidden:
        for cat in categories:
            for item in cat.travelitem_set.all():

                key = f"hidden_checked_{item.id}"
                item.item_checked = int(hidden.get(key, "0"))

                name_key = f"hidden_name_{item.id}"
                if name_key in hidden:
                    item.item_name = hidden.get(name_key)

    # カウント更新
    for cat in categories:
        cat.checked_count = cat.travelitem_set.filter(item_checked=1).count()
        cat.total_count = cat.travelitem_set.count()

    return render(request, "new_travel/template_edit2.html", {
        "template": template,
        "categories": categories,
    })