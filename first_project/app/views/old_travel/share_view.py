from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.dateformat import DateFormat
from app.models import Link
from ...models.template import TravelCategory, TravelItem
from django.urls import reverse


def share_view(request, token):
    link = get_object_or_404(Link, share_token=token)

    # 有効期限チェック
    today = timezone.now().date()
    if link.expiration_date and link.expiration_date < today:
        return render(request, "share/expired.html")

    template = link.template
    travel_info = template.travel_info

    # ---------------------------------------------------------
    # ★ 編集可能リンク（ログイン必須）
    # ---------------------------------------------------------
    if link.permission_type == Link.PermissionType.EDITABLE:

        if not request.user.is_authenticated:
            login_url = reverse("app:login")
            return redirect(f"{login_url}?next=/share/{token}/")


        categories = TravelCategory.objects.filter(template=template)

        return render(request, "old_travel/template_manage.html", {
            "current_template": template,
            "categories": categories,
            "card_travel_info": travel_info,
            "can_edit": True, 
        })

    # ---------------------------------------------------------
    # ★ 閲覧専用リンク
    # ---------------------------------------------------------
    categories = TravelCategory.objects.filter(template=template)

    for cat in categories:
        cat.items = cat.travelitem_set.order_by('item_checked', 'id')
        cat.checked_count_display = cat.checked_count
        cat.total_count_display = cat.total_count

    items = TravelItem.objects.filter(travel_category__template=template)
    total_items = items.count()
    checked_items = items.filter(item_checked=1).count()

    if travel_info.end_date < today:
        status = "済"
    elif total_items > 0 and total_items == checked_items:
        status = "完"
    else:
        status = "未"

    travel_info.status_label = status

    df = DateFormat(link.expiration_date)
    formatted_expiration = df.format('Y.n.j')

    return render(request, "old_travel/travel_detail.html", {
        "travel_info": travel_info,
        "categories": categories,
        "template": template,
        "total_items": total_items,
        "checked_items": checked_items,
        "can_check": True,
        "can_edit": False,
        "is_share_page": True,
        "formatted_expiration": formatted_expiration,
    })