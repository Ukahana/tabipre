from django.shortcuts import render, redirect, get_object_or_404
from app.models import Travel_info, Template
from app.forms import TravelStep2Form, TravelStep1Form, TemplateEditForm

def old_travel_edit2(request, travel_id):
    travel = get_object_or_404(Travel_info, pk=travel_id)
    template = Template.objects.get(travel_info=travel)

    if request.method == "POST":
        # Step1 の情報も一緒に保存したい場合
        form1 = TravelStep1Form(request.POST, instance=travel)
        form2 = TemplateEditForm(request.POST, instance=template)

        # Step2 のフォーム
        form3 = TravelStep2Form(request.POST)

        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            # Step1 保存
            form1.save()
            form2.save()

            # Step2 保存
            travel.location = form3.cleaned_data["location"]
            travel.memo = form3.cleaned_data["memo"]
            travel.transport_other = form3.cleaned_data["transport_other"]

            # ManyToMany の保存
            travel.transport.set(form3.cleaned_data["transport"])

            travel.save()

            return redirect("app:travel_detail", travel_id=travel.id)

    else:
        # 初期値をセット
        form1 = TravelStep1Form(instance=travel)
        form2 = TemplateEditForm(instance=template)

        form3 = TravelStep2Form(initial={
            "location": travel.location,
            "transport_types": travel.transport.all(),
            "transport_other": travel.transport_other,
            "memo": travel.memo,
        })

    return render(request, "tabipre/travel_detail.html", {
        "travel": travel,
        "template": template,
        "form1": form1,
        "form2": form2,
        "form3": form3,
    })