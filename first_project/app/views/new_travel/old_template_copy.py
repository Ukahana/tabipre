from django.shortcuts import render, get_object_or_404, redirect
from ...models.template import Template, TravelCategory, TravelItem
from ...models.travel import Transport, Travelmode



def old_template_copy(request, template_id):
    template = get_object_or_404(Template, id=template_id)

    step2 = request.session.get("copy_step2")
    if not step2:
        return redirect("app:travel_step2")

    if request.method == "POST":

        travel = template.travel_info

        # -------------------------
        # メモ更新（常に更新）
        # -------------------------
        posted_memo = request.POST.get("memo", "").strip()
        travel.memo = posted_memo
        travel.location = step2["location"]
        travel.save()

        # -------------------------
        # 交通手段の更新（常に更新）
        # -------------------------
        Travelmode.objects.filter(travel_info=travel).delete()

        for tid in step2["transport_types"]:
            transport = Transport.objects.get(pk=tid)
            Travelmode.objects.get_or_create(
                travel_info=travel,
                transport=transport,
                defaults={"custom_transport_text": ""}
            )

        other_text = step2["transport_other"].strip()
        if other_text:
            other_transport = Transport.objects.get(
                transport_type=Transport.TransportType.OTHER
            )
            Travelmode.objects.get_or_create(
                travel_info=travel,
                transport=other_transport,
                defaults={"custom_transport_text": other_text}
            )

        # -------------------------
        # カテゴリ削除
        # -------------------------
        delete_cat_id = request.POST.get("delete_category")
        if delete_cat_id and delete_cat_id.isdigit():
            TravelItem.objects.filter(travel_category_id=delete_cat_id).delete()
            TravelCategory.objects.filter(id=delete_cat_id).delete()
            return redirect(request.path)

        # -------------------------
        # 項目削除
        # -------------------------
        delete_item_id = request.POST.get("delete_item")
        if delete_item_id and delete_item_id.isdigit():
            TravelItem.objects.filter(id=delete_item_id).delete()
            return redirect(request.path)

        # -------------------------
        # 項目名の更新（rename_◯◯）
        # -------------------------
        for item in TravelItem.objects.filter(travel_category__template=template):
            new_name = request.POST.get(f"rename_{item.id}", "").strip()
            if new_name and new_name != item.item_name:
                item.item_name = new_name
                item.save()

        # -------------------------
        # チェック状態の更新
        # -------------------------
        for item in TravelItem.objects.filter(travel_category__template=template):
            checked = request.POST.get(f"item_checked_{item.id}")
            item.item_checked = 1 if checked else 0
            item.save()

        # -------------------------
        # 保存して HOME へ
        # -------------------------
        if "save_changes" in request.POST:
            del request.session["copy_step2"]
            return redirect("app:home")

        return redirect(request.path)

    # GET の場合
    categories = TravelCategory.objects.filter(template=template)
    return render(request, "new_travel/old_template.html", {
        "template": template,
        "categories": categories,
    })

