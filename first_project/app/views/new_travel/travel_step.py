from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from ...models.travel import Travel_info, Transport, Travelmode
from ...forms.travel import TravelStep1Form, TravelStep2Form


# -----------------------------
# Step1：旅行基本情報入力
# -----------------------------
@login_required
def travel_create_step1(request):
    if request.method == "POST":
        form = TravelStep1Form(request.POST)
        if form.is_valid():
            travel = form.save(commit=False)
            travel.user = request.user
            travel.location = None  # Step2 で設定
            travel.save()

            # Step2 へ
            return redirect("app:travel_step2", travel_id=travel.travel_info_id)
    else:
        form = TravelStep1Form()

    return render(request, "new_travel/travel_step1.html", {"form": form})


# -----------------------------
# Step2：場所・交通手段・メモ
# -----------------------------
@login_required
def travel_create_step2(request, travel_id):
    travel = get_object_or_404(Travel_info, pk=travel_id)

    if request.method == "POST":
        form = TravelStep2Form(request.POST)
        if form.is_valid():

            # location & memo を保存
            travel.location = form.cleaned_data["location"]
            travel.memo = form.cleaned_data["memo"]
            travel.save()

            # transport（チェックボックス）
            transports = form.cleaned_data["transport"]
            for t in transports:
                Travelmode.objects.create(travel_info=travel, transport=t)

            # その他自由記入
            other = form.cleaned_data["transport_other"]
            if other:
                other_obj = Transport.objects.create(
                    transport_type=Transport.TransportType.OTHER
                )
                Travelmode.objects.create(travel_info=travel, transport=other_obj)

            return redirect("app:travel_detail", travel_id=travel.travel_info_id)

    else:
        form = TravelStep2Form()

    return render(request, "new_travel/travel_step2.html", {
        "form": form,
        "travel": travel,
    })


# -----------------------------
# 完了画面（詳細）
# -----------------------------
@login_required
def travel_detail(request, travel_id):
    travel = get_object_or_404(Travel_info, pk=travel_id)

    # 交通手段一覧
    transports = Travelmode.objects.filter(travel_info=travel)

    return render(request, "app:travel_detail.html", {
        "travel": travel,
        "transports": transports,
    })