from django.shortcuts import render, get_object_or_404, redirect
from ...models.template import Template, TravelCategory, TravelItem
from ...models.travel import  Transport, Travelmode

def old_template_copy(request, template_id):
    template = get_object_or_404(Template, id=template_id)

    # ★ Step2 の内容を取得
    step2 = request.session.get("copy_step2")
    if not step2:
        return redirect("app:travel_step2")

    if request.method == "POST":

        # --- Step2 の memo / location を上書き ---
        travel = template.travel_info
        travel.memo = step2["memo"]
        travel.location = step2["location"]
        travel.save()

        # --- Step2 の交通手段を上書き ---
        transport_ids = step2["transport_types"]
        travel.transport.set(transport_ids)

        # その他の交通手段
        other_text = step2.get("transport_other", "")
        if other_text:
            other_transport = Transport.objects.get(
                transport_type=Transport.TransportType.OTHER
            )
            Travelmode.objects.update_or_create(
                travel_info=travel,
                transport=other_transport,
                defaults={"custom_transport_text": other_text}
            )

        # --- 以下は既存の編集処理（分類削除・項目削除など） ---
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

        # ★ 保存ボタン → home
        if "save_changes" in request.POST:
            del request.session["copy_step2"]
            return redirect("app:home")

        return redirect(request.path)

    categories = TravelCategory.objects.filter(template=template)
    return render(request, "new_travel/old_template.html", {
        "template": template,
        "categories": categories,
    })