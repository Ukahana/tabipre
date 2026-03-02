from django.shortcuts import render, redirect, get_object_or_404
from app.models import Travel_info
from app.models import Template

def TravelCopyModalView(request):
    templates = Template.objects.filter(
        user=request.user
    ).select_related("travel_info").order_by("-travel_info__start_date")

    return render(request, "new_travel/modal/old_travel.html", {
        "templates": templates
    })

