from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ...models.travel import Travel_info
from ...models.template import Template, TravelCategory, TravelItem
from django.http import JsonResponse


def travel_detail(request, travel_id):
    travel_info = get_object_or_404(Travel_info, pk=travel_id)

    template = Template.objects.filter(travel_info=travel_info).order_by('-id').first()

    if template:
        categories = TravelCategory.objects.filter(template=template)
        for cat in categories:
            cat.checked_count = cat.travelitem_set.filter(item_checked=1).count()
            cat.total_count = cat.travelitem_set.count()
    else:
        categories = []

    # --- ここだけスッキリまとめる ---
    items = TravelItem.objects.filter(travel_category__template=template)
    total_items = items.count()
    checked_items = items.filter(item_checked=1).count()

    today = timezone.now().date()
    if travel_info.end_date < today:
        status = "済"
    elif total_items > 0 and total_items == checked_items:
        status = "完"
    else:
        status = "未"

    travel_info.status_label = status

    context = {
        "travel_info": travel_info,
        "categories": categories,
        "template": template,
        "total_items": total_items,
        "checked_items": checked_items,
    }

    return render(request, "old_travel/travel_detail.html", context)

def travel_uncheck_all(request, travel_id):
    TravelItem.objects.filter(
        travel_category__template__travel_info_id=travel_id
    ).update(item_checked=0)
    return redirect("app:travel_detail", travel_id=travel_id)



def toggle_item_checked(request, item_id):
    item = get_object_or_404(TravelItem, pk=item_id)

    item.item_checked = 0 if item.item_checked else 1
    item.save()

    return JsonResponse({"success": True})
