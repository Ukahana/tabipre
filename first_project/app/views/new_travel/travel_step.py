from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q, F
from datetime import datetime, date

from ...models import Travel_info, Transport, Travelmode, Template, TravelCategory, TravelItem
from ...forms.travel import TravelStep1Form, TravelStep2Form
from ...views.new_travel.template_source import template_source
from django.http import QueryDict

# -----------------------------
# Step1：旅行基本情報入力
# -----------------------------
@login_required
def travel_create_step1(request):


    request.session["creating_travel"] = True

    Template.objects.filter(travel_info__isnull=True, user=request.user).delete()

    if request.method == "POST":
        form = TravelStep1Form(request.POST)
        if form.is_valid():

            data = form.cleaned_data.copy()
            data["start_date"] = data["start_date"].isoformat()
            data["end_date"] = data["end_date"].isoformat()

            request.session["travel_step1"] = data
            return redirect("app:travel_step2")

    else:
        form = TravelStep1Form()

    return render(request, "new_travel/travel_step1.html", {"form": form})
# -----------------------------
# Step2：場所・交通手段・メモ
# -----------------------------
@login_required
def travel_step2(request):
    step1_data = request.session.get("travel_step1")
    if not step1_data:
        return redirect("app:travel_step1")

    templates = Template.objects.filter(
    travel_info__user=request.user,
    template_source__isnull=True
    ).order_by('-travel_info__end_date', '-travel_info__start_date')

    today = date.today()
    completed_travel_ids = (
        TravelItem.objects
        .filter(travel_category__template__travel_info__user=request.user)
        .values("travel_category__template__travel_info_id")
        .annotate(
            total=Count("id"),
            done=Count("id", filter=Q(item_checked=TravelItem.ItemChecked.YES))
        )
        .filter(total=F("done"))
        .values_list("travel_category__template__travel_info_id", flat=True)
    )

    for t in templates:
        info = t.travel_info
        if info.end_date < today:
            t.display_status = "済"
        elif info.pk in completed_travel_ids:
            t.display_status = "完"
        else:
            t.display_status = "未"

    # -----------------------------
    # POST
    # -----------------------------
    if request.method == "POST":
        action = request.POST.get("action")

        # -----------------------------
        # open_modal（モーダルを開く）
        # -----------------------------
        if action == "open_modal":
            form = TravelStep2Form(request.POST)

            if not form.is_valid():
                return render(request, "new_travel/travel_step2.html", {
                    "form": form,
                    "step1": step1_data,
                    "templates": templates,
                })

            # QueryDict のまま保存
            request.session["step2_data"] = request.POST.copy()

            return render(request, "new_travel/travel_step2.html", {
                "form": form,
                "step1": step1_data,
                "templates": templates,
                "open_modal": True,
            })

        # -----------------------------
        # copy（前回旅行からコピー）
        # -----------------------------
        if action == "copy" and request.POST.get("old_travel_id"):

            step2_data = request.session.get("step2_data")

            if not step2_data:
                step2_data = request.POST

            from django.http import QueryDict

            def safe_getlist(data, key):
                if hasattr(data, "getlist"):
                    return data.getlist(key)
                value = data.get(key)
                return value if isinstance(value, list) else [value]

            q = QueryDict('', mutable=True)

            for key in step2_data:
                q.setlist(key, safe_getlist(step2_data, key))

            form = TravelStep2Form(q)


            if not form.is_valid():
                return render(request, "new_travel/travel_step2.html", {
                    "form": form,
                    "step1": step1_data,
                    "templates": templates,
                })

            old_id = request.POST.get("old_travel_id")
            old_travel = get_object_or_404(
                Travel_info,
                travel_info_id=old_id,
                user=request.user
            )
            request.session["copy_step2"] = {
                "location": form.cleaned_data["location"],
                "transport_types": [t.pk for t in form.cleaned_data["transport_types"]],
                "transport_other": form.cleaned_data.get("transport_other", "").strip(),
                "memo": form.cleaned_data.get("memo", "").strip(),
            }

            start_date = datetime.strptime(step1_data["start_date"], "%Y-%m-%d").date()
            end_date = datetime.strptime(step1_data["end_date"], "%Y-%m-%d").date()

            new_travel = Travel_info.objects.create(
                user=request.user,
                travel_title=step1_data["travel_title"],
                start_date=start_date,
                end_date=end_date,
                stay_type=step1_data["stay_type"],
                location=form.cleaned_data["location"],
                memo=old_travel.memo,
            )

            # -----------------------------
            # 重複しない交通手段登録（修正版）
            # -----------------------------
            transport_types = {t.pk for t in form.cleaned_data["transport_types"]}
            other_text = form.cleaned_data.get("transport_other", "").strip()

            other_transport = Transport.objects.get(
                transport_type=Transport.TransportType.OTHER
            )

            # OTHER が選択されていて、かつ入力がある場合は通常登録から除外
            if other_transport in transport_types and other_text:
                transport_types.remove(other_transport.pk)

            # 通常の交通手段
            for tid in transport_types:
                transport = Transport.objects.get(pk=tid)
                Travelmode.objects.create(
                    travel_info=travel,
                    transport=transport,
                    custom_transport_text=""
                )

            # OTHER（custom_text あり）
            if other_text:
                Travelmode.objects.create(
                    travel_info=travel,
                    transport=other_transport,
                     custom_transport_text=other_text
                )


            # テンプレート構造コピー
            old_template = Template.objects.get(travel_info=old_travel)
            new_template = Template.objects.create(
                user=request.user,
                travel_info=new_travel,
                source_type=Template.SourceType.FROM_TEMPLATE,
                template_source=old_template
            )

            for cat in old_template.travelcategory_set.all():
                new_cat = TravelCategory.objects.create(
                    template=new_template,
                    category_name=cat.category_name,
                    travel_type=cat.travel_type,
                    category_color=cat.category_color
                )

                for item in cat.travelitem_set.all():
                    TravelItem.objects.create(
                        travel_category=new_cat,
                        item_name=item.item_name,
                        item_checked=item.item_checked
                    )

            request.session["creating_travel"] = False
            del request.session["travel_step1"]
            messages.success(request, "前回の旅行をコピーしました")
            return redirect("app:old_template_copy", template_id=new_template.id)

        # -----------------------------
        # template（通常保存）
        # -----------------------------
        if action == "template":
            form = TravelStep2Form(request.POST)

            if not form.is_valid():
                return render(request, "new_travel/travel_step2.html", {
                    "form": form,
                    "step1": step1_data,
                    "templates": templates,
                })

            start_date = datetime.strptime(step1_data["start_date"], "%Y-%m-%d").date()
            end_date = datetime.strptime(step1_data["end_date"], "%Y-%m-%d").date()

            travel = Travel_info.objects.create(
                user=request.user,
                travel_title=step1_data["travel_title"],
                start_date=start_date,
                end_date=end_date,
                stay_type=step1_data["stay_type"],
                location=form.cleaned_data["location"],
                memo=form.cleaned_data["memo"].strip(),
            )

            # -----------------------------
            #  重複しない交通手段登録（修正版）
            # -----------------------------
            transport_types = {t.pk for t in form.cleaned_data["transport_types"]}
            other_text = form.cleaned_data.get("transport_other", "").strip()

            other_transport = Transport.objects.get(
                transport_type=Transport.TransportType.OTHER
            )

            if other_transport in transport_types and other_text:
                transport_types.remove(other_transport)

            for tid in transport_types:
                transport = Transport.objects.get(pk=tid)
                Travelmode.objects.create(
                    travel_info=travel,
                    transport=transport,
                    custom_transport_text=""
                )

            if other_text:
                Travelmode.objects.create(
                    travel_info=travel,
                    transport=other_transport,
                    custom_transport_text=other_text
                )

            template = template_source(travel, request.user)

            request.session["creating_travel"] = False
            del request.session["travel_step1"]
            messages.success(request, "テンプレートを自動作成しました")
            return redirect("app:template_edit", template_id=template.id)

    # -----------------------------
    # GET
    # -----------------------------
    form = TravelStep2Form()
    return render(request, "new_travel/travel_step2.html", {
        "form": form,
        "step1": step1_data,
        "templates": templates,
    })