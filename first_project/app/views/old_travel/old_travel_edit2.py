from django.shortcuts import render, redirect, get_object_or_404
from app.models import Travel_info, Template, Transport, Travelmode
from app.forms import TravelStep2Form

def old_travel_edit2(request, travel_id):
    travel = get_object_or_404(Travel_info, pk=travel_id)
    template = Template.objects.get(travel_info=travel)

    # OTHER の Transport を取得
    other_transport = Transport.objects.get(
        transport_type=Transport.TransportType.OTHER
    )

    if request.method == "POST":
        form = TravelStep2Form(request.POST)

        if form.is_valid():
            # Step2 保存
            travel.location = form.cleaned_data["location"]
            travel.memo = form.cleaned_data["memo"]
            travel.save()

            # ManyToMany 保存
            travel.transport.set(form.cleaned_data["transport_types"])

            # OTHER の入力処理
            other_text = form.cleaned_data.get("transport_other", "").strip()

            if other_text:
                # OTHER を Travelmode に保存
                Travelmode.objects.update_or_create(
                    travel_info=travel,
                    transport=other_transport,
                    defaults={"custom_transport_text": other_text}
                )
            else:
                # OTHER が空なら削除
                Travelmode.objects.filter(
                    travel_info=travel,
                    transport=other_transport
                ).delete()

            return redirect("app:old_travel_edit2",travel.id)

    else:
        # OTHER の初期値を取得
        other_mode = Travelmode.objects.filter(
            travel_info=travel,
            transport=other_transport
        ).first()

        other_text = other_mode.custom_transport_text if other_mode else ""

        form = TravelStep2Form(initial={
            "location": travel.location,
            "transport_types": travel.transport.all(),
            "transport_other": other_text,
            "memo": travel.memo,
        })

    return render(request, "old_travel/travel_edit2.html", {
        "travel": travel,
        "template": template,
        "form": form,
    })