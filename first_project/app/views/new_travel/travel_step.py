from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from ...models import Travel_info, Transport, Travelmode,Template
from ...forms.travel import TravelStep1Form, TravelStep2Form
from ...views.new_travel.template_source import template_source

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

        if action == "template" and form.is_valid():

            # Travel_info を作成（transport_other は入れない）
            travel = Travel_info.objects.create(
                user=request.user,
                travel_title=step1_data["travel_title"],
                start_date=step1_data["start_date"],
                end_date=step1_data["end_date"],
                stay_type=step1_data["stay_type"],
                location=form.cleaned_data["location"],
                memo=form.cleaned_data["memo"],
            )

            # 選択された交通手段をセット
            travel.transport.set(form.cleaned_data["transport_types"])

            # ★ その他の交通手段が入力されていた場合、Travelmode に保存
            other_text = form.cleaned_data.get("transport_other", "").strip()
            if other_text:
                # OTHER の Transport を取得
                other_transport = Transport.objects.get(
                    transport_type=Transport.TransportType.OTHER
                )

                # Travelmode に custom_transport_text を保存
                Travelmode.objects.update_or_create(
                    travel_info=travel,
                    transport=other_transport,
                    defaults={"custom_transport_text": other_text}
                )

            # Template 作成（分類生成は template_source に任せる）
            template_source(travel, request.user)

            # Step1 の session を削除
            del request.session["travel_step1"]

            return redirect("app:template_edit", template_id=travel.travel_info_id)


        # -----------------------------
        # コピー作成（旧旅行からコピー）
        # -----------------------------
        if action == "copy":
            old_travel_id = request.POST.get("old_travel_id")
            old_travel = get_object_or_404(Travel_info, id=old_travel_id)
            old_template = Template.objects.get(travel_info=old_travel)

            travel = Travel_info.objects.create(
                user=request.user,
                travel_title=step1_data["travel_title"],
                start_date=step1_data["start_date"],
                end_date=step1_data["end_date"],
                stay_type=step1_data["stay_type"],
                location=old_travel.location,
                memo=old_travel.memo,
            )

            # 交通手段コピー
            travel.transport.set(old_travel.transport.all())

            # Travelmode の custom_transport_text もコピー
            for tm in old_travel.travelmode_set.all():
                Travelmode.objects.create(
                    travel_info=travel,
                    transport=tm.transport,
                    custom_transport_text=tm.custom_transport_text
                )

            # Template 作成
            Template.objects.create(
                user=request.user,
                travel_info=travel,
                template_source=old_template.template_source
            )

            del request.session["travel_step1"]

            return redirect("app:template_edit", template_id=travel.travel_info_id)


    else:
        form = TravelStep2Form()

    return render(request, "new_travel/travel_step2.html", {
        "form": form,
        "step1": step1_data,
    })


# -----------------------------
# 完了画面（詳細）
# -----------------------------
@login_required
def travel_detail(request, travel_id):
    travel = get_object_or_404(Travel_info, pk=travel_id)

    # 交通手段一覧
    transports = Travelmode.objects.filter(travel_info=travel)

    return render(request, "new_travel/template_edit.html", {
        "travel": travel,
        "transports": transports,
    })