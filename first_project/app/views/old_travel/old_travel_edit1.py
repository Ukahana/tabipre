from django.shortcuts import render, redirect, get_object_or_404
from app.models import Travel_info, Template
from app.forms import TravelEditForm, TemplateEditForm


def old_travel_edit1(request, travel_id):
    travel = get_object_or_404(Travel_info, pk=travel_id)
    template = Template.objects.get(travel_info=travel)

    if request.method == "POST":
        form = TravelEditForm(request.POST, instance=travel)
        template_form = TemplateEditForm(request.POST, instance=template)

        if form.is_valid() and template_form.is_valid():
            form.save()
            template_form.save()
            return redirect("app:travel", travel_id=travel.id)

    else:
        form = TravelEditForm(instance=travel)
        template_form = TemplateEditForm(instance=template)

    return render(request, "tabipre/travel_detail.html", {
        "travel": travel,
        "template": template,
        "form": form,
        "template_form": template_form,
    })