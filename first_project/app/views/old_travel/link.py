import secrets
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from app.models import Link, Travel_info, Template
from app.forms import LinkForm


def create_link(request, travel_id):
    travel = get_object_or_404(Travel_info, pk=travel_id)
    template = get_object_or_404(Template, travel_info=travel)

    next_day = travel.end_date + timedelta(days=1)

    if request.method == "POST":
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.user = request.user
            link.template = template
            link.share_token = secrets.token_hex(32)

            # 有効期限の設定
            if link.expiration_type == Link.ExpirationType.ONE_MONTH:
                link.expiration_date = timezone.now().date() + timedelta(days=30)

            elif link.expiration_type == Link.ExpirationType.AFTER_TRIP:
                link.expiration_date = next_day

            else:  # USER_INPUT
                link.expiration_date = form.cleaned_data["expiration_date"]

            link.save()

            # モーダル用の共有URL
            share_url = request.build_absolute_uri(f"/share/{link.share_token}/")

            # ★ redirect しない → モーダルを表示するため
            return render(request, "old_travel/create_link.html", {
                "form": LinkForm(),          # 空フォームに戻す
                "template": template,
                "travel": travel,
                "next_day": next_day,
                "link": link,                # ★ モーダル用
                "share_url": share_url,      # ★ モーダル用
                "show_modal": True,          # ★ モーダル表示フラグ
            })

    else:
        form = LinkForm()

    # GET の場合（モーダルなし）
    return render(request, "old_travel/create_link.html", {
        "form": form,
        "template": template,
        "travel": travel,
        "next_day": next_day,
        "show_modal": False,   # ← ★ これが絶対必要！
    })