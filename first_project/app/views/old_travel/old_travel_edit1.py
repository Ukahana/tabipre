from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from app.models import Travel_info, Template
from app.forms import TravelStep1Form

from datetime import datetime

def old_travel_edit1(request, travel_id):
    travel = get_object_or_404(Travel_info, pk=travel_id)

    if request.method == "POST":
        form = TravelStep1Form(request.POST, instance=travel)


        if form.is_valid():
            data = form.cleaned_data

            start = data["start_date"]
            end = data["end_date"]


            # -----------------------------
            # ★ エラー処理（view側）
            # -----------------------------

            # 終了日が開始日より前
            if end < start:
                form.add_error("end_date", "終了日は開始日より後の日付を選択してください。")
                return render(request, "old_travel/travel_edit1.html", {
                    "form": form,
                    "travel": travel,
                    "stay_nights": (travel.end_date - travel.start_date).days,
                    "stay_days": (travel.end_date - travel.start_date).days + 1,
                })

            # 開始日・終了日が未入力（Django が自動で検出するが念のため）
            if not start or not end:
                form.add_error("start_date", "開始日と終了日を入力してください。")
                return render(request, "old_travel/travel_edit1.html", {
                    "form": form,
                    "travel": travel,
                    "stay_nights": 0,
                    "stay_days": 1,
                })

            # 旅行期間が長すぎる（例：60日以上）
            if (end - start).days > 60:
                form.add_error("end_date", "旅行期間が長すぎます。60日以内にしてください。")
                return render(request, "old_travel/travel_edit1.html", {
                    "form": form,
                    "travel": travel,
                    "stay_nights": 0,
                    "stay_days": 1,
                })

            # -----------------------------
            # ★ エラーなし → session に保存
            # -----------------------------
            session_data = data.copy()
            session_data["start_date"] = start.isoformat()
            session_data["end_date"] = end.isoformat()

            session_data["stay_nights"] = (end - start).days
            session_data["stay_days"] = (end - start).days + 1

            request.session["edit_travel"] = session_data

            return redirect("app:old_travel_edit2", travel_id=travel_id)

    else:
        form = TravelStep1Form(instance=travel)

    stay_nights = (travel.end_date - travel.start_date).days
    stay_days = stay_nights + 1

    return render(request, "old_travel/travel_edit1.html", {
        "form": form,
        "travel": travel,
        "stay_nights": stay_nights,
        "stay_days": stay_days,
    })