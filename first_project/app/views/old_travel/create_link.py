import secrets
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from dateutil.relativedelta import relativedelta
from app.models import Link, Travel_info, Template
from app.forms import LinkForm
from ...models.template import Template, TravelCategory, TravelItem
from django.urls import reverse

def create_link(request, travel_id):
    travel = get_object_or_404(Travel_info, pk=travel_id)

    original_template = Template.objects.filter(
        travel_info=travel,
    ).first()

    existing_link = Link.objects.filter(
        template__template_source=original_template
    ).first()

    next_day = travel.end_date + timedelta(days=1)
    today = timezone.now().date()
    one_month_later = today + relativedelta(months=1)

    # ▼ 旅行終了日の翌日が過去かどうか
    is_after_trip_expired = next_day < today

    expiration_choices = [
        (0, "1か月間有効："),
        (1, "旅行終了日の翌日まで："),
        (2, "日付を指定する"),
    ]

    # -------------------------
    # GET
    # -------------------------
    if request.method == "GET":
        form = LinkForm(initial={
            "permission_type": Link.PermissionType.READ_ONLY,
            "expiration_type": Link.ExpirationType.ONE_MONTH,
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
            "is_after_trip_expired": is_after_trip_expired,
        })

    # -------------------------
    # POST
    # -------------------------
    form = LinkForm(request.POST)
    form.fields["expiration_type"].choices = expiration_choices

    # 既存リンクチェック
    if existing_link:
        form.add_error(None, "この旅行のリンクはすでに発行されています")
        return render(request, "old_travel/create_link.html", {
            "form": form,
            "template": original_template,
            "travel": travel,
            "next_day": next_day,
            "one_month_later": one_month_later,
            "show_modal": False,
            "is_after_trip_expired": is_after_trip_expired,
        })

    # バリデーション NG
    if not form.is_valid():
        return render(request, "old_travel/create_link.html", {
            "form": form,
            "template": original_template,
            "travel": travel,
            "next_day": next_day,
            "one_month_later": one_month_later,
            "show_modal": False,
            "is_after_trip_expired": is_after_trip_expired,
        })

    # ▼ 不正に「旅行終了日の翌日」を選んだ場合の保険
    if form.cleaned_data["expiration_type"] == Link.ExpirationType.AFTER_TRIP:
        if is_after_trip_expired:
            form.add_error("expiration_type", "旅行終了日の翌日はすでに過ぎています。")
            return render(request, "old_travel/create_link.html", {
                "form": form,
                "template": original_template,
                "travel": travel,
                "next_day": next_day,
                "one_month_later": one_month_later,
                "show_modal": False,
                "is_after_trip_expired": is_after_trip_expired,
            })

    # -------------------------
    # コピー作成
    # -------------------------
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
                item_checked=item.item_checked,
            )

    # -------------------------
    # リンク作成
    # -------------------------
    link = form.save(commit=False)
    link.user = request.user
    link.template = copied_template
    link.share_token = secrets.token_urlsafe(9)[:12]

    if link.expiration_type == Link.ExpirationType.ONE_MONTH:
        link.expiration_date = one_month_later
    elif link.expiration_type == Link.ExpirationType.AFTER_TRIP:
        link.expiration_date = next_day

    link.save()
    share_url = request.build_absolute_uri(
    reverse("app:share_view", args=[link.share_token])
    )

    return render(request, "old_travel/create_link.html", {
        "form": form,
        "template": original_template,
        "travel": travel,
        "next_day": next_day,
        "one_month_later": one_month_later,
        "link": link,
        "share_url": share_url,
        "show_modal": True,
        "is_after_trip_expired": is_after_trip_expired,
    })
