import secrets
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from dateutil.relativedelta import relativedelta
from app.models import Link, Travel_info, Template
from app.forms import LinkForm
from ...models.template import Template, TravelCategory, TravelItem
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

import secrets
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from dateutil.relativedelta import relativedelta
from app.models import Link, Travel_info, Template
from app.forms import LinkForm
from ...models.template import Template, TravelCategory, TravelItem
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.utils.dateformat import DateFormat
def create_link(request, travel_id):
    travel = get_object_or_404(Travel_info, pk=travel_id)

    # 元テンプレート（template_source=None）
    original_template = Template.objects.filter(
        travel_info=travel,
        template_source__isnull=True
    ).first()

    # 既存リンク（2回目以降）
    existing_link = Link.objects.filter(
        template__template_source=original_template
    ).first()

    next_day = travel.end_date + timedelta(days=1)
    one_month_later = timezone.now().date() + relativedelta(months=1)

    expiration_choices = [
        (0, "1か月間有効："),
        (1, "旅行終了日の翌日まで："),
        (2, "日付を指定する"),
    ]

    # ▼ GET：いつでも画面表示（2回目でも日付は出す）
    if request.method == "GET":
        form = LinkForm(initial={
            "expiration_type": 0,
            "expiration_date": one_month_later,
        })
        form.fields["expiration_type"].choices = expiration_choices

        return render(request, "old_travel/create_link.html", {
            "form": form,
            "template": original_template,
            "travel": travel,
            "next_day": next_day,
            "one_month_later": one_month_later,
            "existing_link": existing_link,
            "show_modal": False,
        })

    # ▼ POST：リンク発行
    form = LinkForm(request.POST)
    form.fields["expiration_type"].choices = expiration_choices

    # ★ ① まず既存リンクチェック（2回目以降）
    if existing_link:
        form.add_error(None, "この旅行の共有リンクはすでに作成されています。")
        return render(request, "old_travel/create_link.html", {
            "form": form,
            "template": original_template,
            "travel": travel,
            "next_day": next_day,
            "one_month_later": one_month_later,
            "show_modal": False,
        })

    # ★ ② 1回目だけ通常バリデーション（必須チェックなど）
    if not form.is_valid():
        return render(request, "old_travel/create_link.html", {
            "form": form,
            "template": original_template,
            "travel": travel,
            "next_day": next_day,
            "one_month_later": one_month_later,
            "show_modal": False,
        })

    # ▼ ★★ コピー処理（1回目のみ実行）★★
    copied_template = Template.objects.create(
        user=original_template.user,
        travel_info=original_template.travel_info,
        source_type=original_template.source_type,
        template_source=original_template,
    )

    for cat in original_template.travelcategory_set.all():
        new_cat = TravelCategory.objects.create(
            template=copied_template,
            category_name=cat.category_name,
            travel_type=cat.travel_type,
            category_color=cat.category_color,
        )
        for item in cat.travelitem_set.all():
            TravelItem.objects.create(
                travel_category=new_cat,
                item_name=item.item_name,
                item_checked=0,
            )

    # ▼ Link 保存
    link = form.save(commit=False)
    link.user = request.user
    link.template = copied_template
    link.share_token = secrets.token_urlsafe(9)[:12]

    if link.expiration_type == Link.ExpirationType.ONE_MONTH:
        link.expiration_date = one_month_later
    elif link.expiration_type == Link.ExpirationType.AFTER_TRIP:
        link.expiration_date = next_day

    link.save()

    share_url = request.build_absolute_uri(f"/share/{link.share_token}/")

    return render(request, "old_travel/create_link.html", {
        "form": form,
        "template": original_template,
        "travel": travel,
        "next_day": next_day,
        "one_month_later": one_month_later,
        "link": link,
        "share_url": share_url,
        "show_modal": True,
    })


def share_view(request, token):
    link = get_object_or_404(Link, share_token=token)

    # 有効期限チェック
    today = timezone.now().date()
    if link.expiration_date and link.expiration_date < today:
        return render(request, "share/expired.html")

    # ★ コピーされたテンプレートを使う
    template = link.template
    travel_info = template.travel_info
    
    # ★ カテゴリと項目を travel_detail と同じ構造で取得
    if template:
        categories = TravelCategory.objects.filter(template=template)

        for cat in categories:
            cat.items = cat.travelitem_set.order_by('item_checked', 'id')
            cat.checked_count_display = cat.checked_count
            cat.total_count_display = cat.total_count
    else:
        categories = []

    # ★ ステータス計算（travel_detail と同じ）
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

    # ★ 閲覧専用フラグ
    can_check = True
    can_edit = False  # 共有リンクは編集不可

    return render(request, "old_travel/travel_detail.html", {
        "travel_info": travel_info,
        "categories": categories,
        "template": template,
        "total_items": total_items,
        "checked_items": checked_items,
        "can_check": can_check,
        "can_edit": can_edit,
        "is_share_page": True,
        "formatted_expiration": link.formatted_expiration,
    })

@require_POST
def toggle_item_checked_share(request, token, item_id):
    link = get_object_or_404(Link, share_token=token)
    template = link.template  # ← コピーされたテンプレート

    item = get_object_or_404(
        TravelItem,
        pk=item_id,
        travel_category__template=template  # ← ★ コピー側だけ更新！
    )

    data = json.loads(request.body)
    checked = data.get("checked", False)

    item.item_checked = 1 if checked else 0
    item.save()

    return JsonResponse({"success": True})


def share_view(request, token):
    link = get_object_or_404(Link, share_token=token)

    # 有効期限チェック
    today = timezone.now().date()
    if link.expiration_date and link.expiration_date < today:
        return render(request, "share/expired.html")

    # ★ コピーされたテンプレートを使う
    template = link.template
    travel_info = template.travel_info
    
    # ★ カテゴリと項目を travel_detail と同じ構造で取得
    if template:
        categories = TravelCategory.objects.filter(template=template)

        for cat in categories:
            cat.items = cat.travelitem_set.order_by('item_checked', 'id')
            cat.checked_count_display = cat.checked_count
            cat.total_count_display = cat.total_count
    else:
        categories = []

    # ★ ステータス計算（travel_detail と同じ）
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

    # ★ 閲覧専用フラグ
    can_check = True
    can_edit = False  # 共有リンクは編集不可

    # 有効期限の整形
    if link.expiration_date:
        df = DateFormat(link.expiration_date)
        formatted_expiration = df.format('Y.n.j')
    else:
        formatted_expiration = "設定なし"
        
    return render(request, "old_travel/travel_detail.html", {
        "travel_info": travel_info,
        "categories": categories,
        "template": template,
        "total_items": total_items,
        "checked_items": checked_items,
        "can_check": can_check,
        "can_edit": can_edit,
        "is_share_page": True,
        "formatted_expiration": formatted_expiration,
    })

@require_POST
def toggle_item_checked_share(request, token, item_id):
    link = get_object_or_404(Link, share_token=token)
    template = link.template  # ← コピーされたテンプレート

    item = get_object_or_404(
        TravelItem,
        pk=item_id,
        travel_category__template=template  # ← ★ コピー側だけ更新！
    )

    data = json.loads(request.body)
    checked = data.get("checked", False)

    item.item_checked = 1 if checked else 0
    item.save()

    return JsonResponse({"success": True})