from django.shortcuts import render, redirect, get_object_or_404
from app.models import Travel_info, Template, Transport, Travelmode
from app.forms import TravelStep2Form

def old_travel_edit2(request, travel_id):
    travel = get_object_or_404(Travel_info, pk=travel_id)
    template = Template.objects.get(travel_info=travel)

    if request.method == "POST":
        form = TravelStep2Form(request.POST, instance=travel)

        if form.is_valid():

            # Step1 の編集内容を session から反映
            session_data = request.session.get("edit_travel")
            if session_data:
                travel.travel_title = session_data["travel_title"]
                travel.start_date = session_data["start_date"]
                travel.end_date = session_data["end_date"]
                travel.save()

            # Step2 の保存
            updated_travel = form.save(commit=False)
            updated_travel.save()

            # 交通手段の保存
            updated_travel.transport.set(form.cleaned_data["transport_types"])

            # OTHER の保存
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

            # session の削除
            if "edit_travel" in request.session:
                del request.session["edit_travel"]

            return redirect("app:home")

    else:
        form = TravelStep2Form(instance=travel)

    return render(request, "old_travel/travel_edit2.html", {
        "travel": travel,
        "template": template,
        "form": form,
    })