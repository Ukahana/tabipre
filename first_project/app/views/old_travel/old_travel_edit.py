from django.shortcuts import render, redirect, get_object_or_404
from datetime import date, datetime  
from app.models import Travel_info, Template, Transport, Travelmode
from app.forms import TravelStep1Form, TravelStep2Form


# ---------------------------------------------------------
# ★ Step1：旅行基本情報の編集（タイトル・日付・宿泊タイプ）
# ---------------------------------------------------------
def old_travel_edit1(request, travel_id):
    travel = get_object_or_404(Travel_info, pk=travel_id)

    def calc_stay(travel_obj):
        nights = (travel_obj.end_date - travel_obj.start_date).days
        return nights, nights + 1

    if request.method == "POST":
        form = TravelStep1Form(request.POST, instance=travel)

        if form.is_valid():
            start = form.cleaned_data["start_date"]
            end = form.cleaned_data["end_date"]

            # Step1 の内容を session に保存（DB 保存は Step2 でまとめて）
            request.session["edit_travel"] = {
                "travel_title": form.cleaned_data["travel_title"],
                "start_date": start.isoformat(),
                "end_date": end.isoformat(),
                "stay_type": form.cleaned_data["stay_type"],
            }

            return redirect("app:old_travel_edit2", travel_id=travel_id)

    else:
        form = TravelStep1Form(instance=travel)

    stay_nights, stay_days = calc_stay(travel)

    return render(request, "old_travel/travel_edit1.html", {
        "form": form,
        "travel": travel,
        "stay_nights": stay_nights,
        "stay_days": stay_days,
        "stay_type": form.instance.stay_type,
    })


# ---------------------------------------------------------
# ★ Step2：旅行詳細情報の編集（交通手段・メモ・場所）
# ---------------------------------------------------------
def old_travel_edit2(request, travel_id):
    travel = get_object_or_404(Travel_info, pk=travel_id)
    template = Template.objects.get(travel_info=travel)

    # ★ カテゴリ取得（必須）
    categories = template.travelcategory_set.all()

    session_data = request.session.get("edit_travel")
    if not session_data:
        return redirect("app:old_travel_edit1", travel_id=travel_id)

    start_date = datetime.strptime(session_data["start_date"], "%Y-%m-%d").date()
    end_date = datetime.strptime(session_data["end_date"], "%Y-%m-%d").date()

    if request.method == "GET":
        form = TravelStep2Form(instance=travel)
        return render(request, "old_travel/travel_edit2.html", {
            "travel": travel,
            "template": template,
            "form": form,
            "categories": categories,  
            "step1": session_data,
        })

    form = TravelStep2Form(request.POST, instance=travel)

    if form.is_valid():
        travel.travel_title = session_data["travel_title"]
        travel.start_date = start_date
        travel.end_date = end_date
        travel.stay_type = session_data["stay_type"]

        travel = form.save(commit=False)
        travel.full_clean()
        travel.save()

        template.travel_info = travel
        template.save()

        travel.transport.set(form.cleaned_data["transport_types"])

        other_transport = Transport.objects.get(
            transport_type=Transport.TransportType.OTHER
        )
        other_text = form.cleaned_data.get("transport_other", "").strip()

        if other_text:
            Travelmode.objects.update_or_create(
                travel_info=travel,
                transport=other_transport,
                defaults={"custom_transport_text": other_text}
            )
        else:
            Travelmode.objects.filter(
                travel_info=travel,
                transport=other_transport
            ).delete()

        request.session.pop("edit_travel", None)

        return redirect("app:home")

    return render(request, "old_travel/travel_edit2.html", {
        "travel": travel,
        "template": template,
        "form": form,
        "categories": categories,  
        "step1": session_data,
    })