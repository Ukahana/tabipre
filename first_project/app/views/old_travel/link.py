import secrets
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from app.models import Link, Template
from app.forms import LinkForm

def create_link(request, template_id):
    template = get_object_or_404(Template, id=template_id)

    if request.method == "POST":
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.user = request.user
            link.template = template
            link.share_token = secrets.token_hex(32)

            # 有効期限の自動計算
            if link.expiration_type == Link.ExpirationType.ONE_MONTH:
                link.expiration_date = timezone.now().date() + timedelta(days=30)

            elif link.expiration_type == Link.ExpirationType.AFTER_TRIP:
                # Template に end_date がある前提
                link.expiration_date = template.end_date + timedelta(days=1)

            # USER_INPUT の場合はフォームの値をそのまま使う

            link.save()
            return redirect("link_created", link_id=link.id)

    else:
        form = LinkForm()

    return render(request, "link/create_link.html", {
        "form": form,
        "template": template,
    })
    

def link_created(request, link_id):
    link = get_object_or_404(Link, id=link_id)

    share_url = request.build_absolute_uri(f"/share/{link.share_token}/")

    return render(request, "link/link_created.html", {
        "link": link,
        "share_url": share_url,
    })

