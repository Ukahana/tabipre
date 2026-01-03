from django.shortcuts import render, get_object_or_404
from ...models.travel import Travel_info
from ...models.template import Template, TravelCategory, TravelItem

def travel_detail(request, travel_id):
    travel = get_object_or_404(Travel_info, pk=travel_id)

    # 旅行に紐づくテンプレートを取得（1旅行に1テンプレート前提）
    template = Template.objects.get(travel_info=travel)

    # 分類一覧
    categories = TravelCategory.objects.filter(template=template)

    # チェック数計算
    total_items = TravelItem.objects.filter(
        travel_category__template=template
    ).count()

    checked_items = TravelItem.objects.filter(
        travel_category__template=template,
        item_checked=TravelItem.ItemChecked.YES
    ).count()

    context = {
        "travel": travel,
        "categories": categories,
        "checked_items": checked_items,
        "total_items": total_items,
    }

    return render(request, "tabipre/travel_detail.html", context)

