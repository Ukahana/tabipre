from django.shortcuts import render, redirect, get_object_or_404
from app.models import Travel_info
from app.forms import TravelStep1Form
from datetime import date


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

            request.session["edit_travel"] = {
                "travel_title": form.cleaned_data["travel_title"],
                "start_date": start.isoformat(),
                "end_date": end.isoformat(),
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
    })