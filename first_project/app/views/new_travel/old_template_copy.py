from django.shortcuts import render, get_object_or_404, redirect
from ...models.template import Template, TravelCategory, TravelItem
from ...models.travel import  Transport, Travelmode

def old_template_copy(request, template_id):
    template = get_object_or_404(Template, id=template_id)

    step2 = request.session.get("copy_step2")
    if not step2:
        return redirect("app:travel_step2")

    if request.method == "POST":

        travel = template.travel_info
        
        # ★ メモをフォームから反映（ここを追加）
        posted_memo = request.POST.get("memo", "").strip()
        travel.memo = posted_memo

        # ★ 場所の分類は Step2 の入力を反映
        travel.location = step2["location"]
        travel.save()

        # ★ 交通手段を Step2 の内容で上書き
        Travelmode.objects.filter(travel_info=travel).delete()

        # 通常の交通手段
        for tid in step2["transport_types"]:
            transport = Transport.objects.get(pk=tid)
            Travelmode.objects.create(
                travel_info=travel,
                transport=transport,
                custom_transport_text=""
            )

        # その他の交通手段
        other_text = step2.get("transport_other", "").strip()
        if other_text:
            other_transport = Transport.objects.get(
                transport_type=Transport.TransportType.OTHER
            )
            Travelmode.objects.create(
                travel_info=travel,
                transport=other_transport,
                custom_transport_text=other_text
            )

        # --- 以下は既存の編集処理 ---
        delete_cat_id = request.POST.get("delete_category")
        if delete_cat_id and delete_cat_id.isdigit():
            TravelItem.objects.filter(travel_category_id=delete_cat_id).delete()
            TravelCategory.objects.filter(id=delete_cat_id).delete()
            return redirect(request.path)

        delete_id = request.POST.get("delete_item")
        if delete_id and delete_id.isdigit():
            TravelItem.objects.filter(id=delete_id).delete()
            return redirect(request.path)

        edit_item_id = request.POST.get("edit_item_id")
        if edit_item_id and edit_item_id.isdigit():
            item = TravelItem.objects.get(id=edit_item_id)
            new_name = request.POST.get("item_name")
            if new_name:
                item.item_name = new_name
                item.save()
            return redirect(request.path)

        for item in TravelItem.objects.filter(travel_category__template=template):
            checked = request.POST.get(f"item_checked_{item.id}")
            item.item_checked = 1 if checked else 0
            item.save()

        if "save_changes" in request.POST:
            del request.session["copy_step2"]
            return redirect("app:home")

        return redirect(request.path)

    categories = TravelCategory.objects.filter(template=template)
    return render(request, "new_travel/old_template.html", {
        "template": template,
        "categories": categories,
        "step2_memo": step2.get("memo", ""),
    })