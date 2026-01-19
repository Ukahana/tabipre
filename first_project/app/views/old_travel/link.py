import secrets
from datetime import timedelta, datetime
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

    # ▼ GET のとき：初期値をセット
    if request.method == "GET":
        form = LinkForm(initial={
            "expiration_type": Link.ExpirationType.ONE_MONTH,
            "expiration_date": one_month_later,
        })
        return render(request, "old_travel/create_link.html", {
            "form": form,
            "template": template,
            "travel": travel,
            "next_day": next_day,
            "one_month_later": one_month_later,
            "show_modal": False,
        })

    # ▼ POST のとき
    form = LinkForm(request.POST)
    if not form.is_valid():
        return render(request, "old_travel/create_link.html", {
            "form": form,
            "template": template,
            "travel": travel,
            "next_day": next_day,
            "one_month_later": one_month_later,
            "show_modal": False,
        })

    link = form.save(commit=False)
    link.user = request.user
    link.template = template
    link.share_token = secrets.token_hex(32)

    expiration_type = link.expiration_type
    raw_date = form.cleaned_data.get("expiration_date")

    # ▼ expiration_type に応じて設定
    if expiration_type == Link.ExpirationType.ONE_MONTH:
        link.expiration_date = one_month_later

    elif expiration_type == Link.ExpirationType.AFTER_TRIP:
        link.expiration_date = next_day

    else:  # USER_INPUT
        if not raw_date:
            form.add_error("expiration_date", "日付を入力してください")
            return render(request, "old_travel/create_link.html", {
                "form": form,
                "template": template,
                "travel": travel,
                "next_day": next_day,
                "one_month_later": one_month_later,
                "show_modal": False,
            })

        # 区切り文字を統一
        normalized = raw_date.replace("/", "-").replace(".", "-")
        parts = normalized.split("-")

        try:
            if len(parts) == 3:
                year, month, day = parts
            elif len(parts) == 2:
                year = str(timezone.now().year)
                month, day = parts
            else:
                raise ValueError

            parsed = datetime(int(year), int(month), int(day)).date()

        except ValueError:
            form.add_error("expiration_date", "正しい日付を入力してください（例: 2/5）")
            return render(request, "old_travel/create_link.html", {
                "form": form,
                "template": template,
                "travel": travel,
                "next_day": next_day,
                "one_month_later": one_month_later,
                "show_modal": False,
            })

        link.expiration_date = parsed

    link.save()

    share_url = request.build_absolute_uri(f"/share/{link.share_token}/")

    return render(request, "old_travel/create_link.html", {
        "form": LinkForm(),
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
    