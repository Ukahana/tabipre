import secrets
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from dateutil.relativedelta import relativedelta
from app.models import Link, Travel_info, Template
from app.forms import LinkForm


def create_link(request, travel_id):
    travel = get_object_or_404(Travel_info, pk=travel_id)
    template = get_object_or_404(Template, travel_info=travel)

    next_day = travel.end_date + timedelta(days=1)
    one_month_later = timezone.now().date() + relativedelta(months=1)

    expiration_choices = [
    (0, "1か月間有効："),
    (1, "旅行終了日の翌日まで："),
    (2, "日付を指定する"),
    ]

    # ▼ GET：初期値セット
    if request.method == "GET":
        form = LinkForm(initial={
            "expiration_type": 0,
            "expiration_date": one_month_later,
        })

        form.fields["expiration_type"].choices = expiration_choices

        return render(request, "old_travel/create_link.html", {
            "form": form,
            "template": template,
            "travel": travel,
            "next_day": next_day,
            "one_month_later": one_month_later,
            "show_modal": False,
        })

    # ▼ POST
    form = LinkForm(request.POST)
    form.fields["expiration_type"].choices = expiration_choices

    if not form.is_valid():
        return render(request, "old_travel/create_link.html", {
            "form": form,
            "template": template,
            "travel": travel,
            "next_day": next_day,
            "one_month_later": one_month_later,
            "show_modal": False,
        })

    # ▼ 保存処理
    link = form.save(commit=False)
    link.user = request.user
    link.template = template
    link.share_token = secrets.token_urlsafe(9)[:12]

    # expiration_type に応じて expiration_date を上書き
    if link.expiration_type == Link.ExpirationType.ONE_MONTH:
        link.expiration_date = one_month_later
    elif link.expiration_type == Link.ExpirationType.AFTER_TRIP:
        link.expiration_date = next_day
    # USER_INPUT の場合はフォーム側でパース済みの値をそのまま使う

    link.save()

    share_url = request.build_absolute_uri(f"/share/{link.share_token}/")

    # 再表示用フォーム（choices 再設定）
    new_form = LinkForm(initial={
    "expiration_type": link.expiration_type,  
    "expiration_date": link.expiration_date,
    })
    
    new_form.fields["expiration_type"].choices = expiration_choices


    return render(request, "old_travel/create_link.html", {
        "form": new_form,
        "template": template,
        "travel": travel,
        "next_day": next_day,
        "one_month_later": one_month_later,
        "link": link,
        "share_url": share_url,
        "show_modal": True,
    })


def share_view(request, token):
    link = get_object_or_404(Link, share_token=token)

    today = timezone.now().date()
    if link.expiration_date and link.expiration_date < today:
        return render(request, "share/expired.html", {
            "link": link,
        })

    template = link.template
    travel = template.travel_info

    return render(request, "share/share_page.html", {
        "link": link,
        "template": template,
        "travel": travel,
    })