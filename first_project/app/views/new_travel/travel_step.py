from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ...models import Travel_info, Transport, Travelmode,Template,TravelCategory,TravelItem
from ...forms.travel import TravelStep1Form, TravelStep2Form
from ...views.new_travel.template_source import template_source
from datetime import datetime


# -----------------------------
# Step1：旅行基本情報入力
# -----------------------------
@login_required
def travel_create_step1(request):
    if request.method == "POST":
        form = TravelStep1Form(request.POST)
        if form.is_valid():

            data = form.cleaned_data.copy()
            data["start_date"] = data["start_date"].isoformat()
            data["end_date"] = data["end_date"].isoformat()

            request.session["travel_step1"] = data
            return redirect("app:travel_step2")

    else:
        form = TravelStep1Form()

    return render(request, "new_travel/travel_step1.html", {"form": form})
# -----------------------------
# Step2：場所・交通手段・メモ
# -----------------------------
@login_required
def travel_step2(request):
    # Step1 のデータを session から取得
    step1_data = request.session.get("travel_step1")

    if not step1_data:
        return redirect("app:travel_step1")

    if request.method == "POST":
        action = request.POST.get("action")
        form = TravelStep2Form(request.POST)

        # -----------------------------
        # テンプレート作成
        # -----------------------------
        if action == "template" and form.is_valid():

            # ★ 文字列 → date に変換（ここが重要）
            start_date = datetime.strptime(step1_data["start_date"], "%Y-%m-%d").date()
            end_date = datetime.strptime(step1_data["end_date"], "%Y-%m-%d").date()

            # Travel_info 作成
            travel = Travel_info.objects.create(
                user=request.user,
                travel_title=step1_data["travel_title"],
                start_date=start_date,
                end_date=end_date,
                stay_type=step1_data["stay_type"],
                location=form.cleaned_data["location"],
                memo=form.cleaned_data["memo"],
            )

            # 選択された交通手段をセット
            travel.transport.set(form.cleaned_data["transport_types"])

            # その他の交通手段
            other_text = form.cleaned_data.get("transport_other", "").strip()
            if other_text:
                other_transport = Transport.objects.get(
                    transport_type=Transport.TransportType.OTHER
                )
                Travelmode.objects.update_or_create(
                    travel_info=travel,
                    transport=other_transport,
                    defaults={"custom_transport_text": other_text}
                )

            # Template 作成
            template = template_source(travel, request.user)

            del request.session["travel_step1"]
            messages.success(request, "テンプレートを作成しました")
            return redirect("app:template_edit", template_id=template.id)

        # -----------------------------
        # コピー作成（旧旅行からコピー）
        # -----------------------------
        if action == "copy":
            old_travel_id = request.POST.get("old_travel_id")
            old_travel = get_object_or_404(Travel_info, travel_info_id=old_travel_id)
            old_template = Template.objects.get(travel_info=old_travel)

            # ★ ここも session → date に変換
            start_date = datetime.strptime(step1_data["start_date"], "%Y-%m-%d").date()
            end_date = datetime.strptime(step1_data["end_date"], "%Y-%m-%d").date()

            travel = Travel_info.objects.create(
                user=request.user,
                travel_title=step1_data["travel_title"],
                start_date=start_date,
                end_date=end_date,
                location=step1_data["location"],
                memo=step1_data.get("memo", "")
            )

            # Travelmode コピー
            for tm in old_travel.travelmode_set.all():
                Travelmode.objects.update_or_create(
                    travel_info=travel,
                    transport=tm.transport,
                    defaults={"custom_transport_text": tm.custom_transport_text}
                )

            # Template コピー
            new_template = Template.objects.create(
                user=request.user,
                travel_info=travel,
                source_type=Template.SourceType.FROM_TEMPLATE,
                template_source=old_template,
            )

            # カテゴリ & アイテムコピー
            old_categories = TravelCategory.objects.filter(template=old_template)

            for old_cat in old_categories:
                new_cat = TravelCategory.objects.create(
                    template=new_template,
                    category_name=old_cat.category_name,
                    category_color=old_cat.category_color,
                    travel_type=old_cat.travel_type,
                )

                for old_item in old_cat.travelitem_set.all():
                    TravelItem.objects.create(
                        travel_category=new_cat,
                        item_name=old_item.item_name,
                        item_checked=old_item.item_checked,
                    )

            del request.session["travel_step1"]
            return redirect("app:old_template_edit", template_id=new_template.id)

    else:
        form = TravelStep2Form()

    templates = Template.objects.filter(travel_info__user=request.user)

    return render(request, "new_travel/travel_step2.html", {
        "form": form,
        "step1": step1_data,
        "templates": templates,
    })


# -----------------------------
# 完了画面（詳細）
# -----------------------------
@login_required
def travel_detail(request, travel_id):
    travel = get_object_or_404(Travel_info, pk=travel_id)

    # 交通手段一覧
    transports = Travelmode.objects.filter(travel_info=travel)

    return render(request, "new_travel/template_detail.html", {
        "travel": travel,
        "transports": transports,
    })
    