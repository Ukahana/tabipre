from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q, F
from datetime import datetime, date

from ...models import Travel_info, Transport, Travelmode, Template, TravelCategory, TravelItem
from ...forms.travel import TravelStep1Form, TravelStep2Form
from ...views.new_travel.template_source import template_source


# -----------------------------
# Step1：旅行基本情報入力
# -----------------------------
@login_required
def travel_create_step1(request):

    # 新規旅行作成開始フラグ ON
    request.session["creating_travel"] = True

    # creating_travel=True のときだけ下書きを削除
    # ※ is_draft を廃止したので travel_info が紐づいていないテンプレートだけ削除
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

    if request.method == "POST":
        action = request.POST.get("action")
        form = TravelStep2Form(request.POST)

        # -----------------------------
        # 新規テンプレート作成
        # -----------------------------
        if action == "template" and form.is_valid():

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

            travel.transport.set(form.cleaned_data["transport_types"])

            other_text = form.cleaned_data.get("transport_other", "").strip()
            if other_text:
                other_transport = Transport.objects.get(
                    transport_type=Transport.TransportType.OTHER
                )
                Travelmode.objects.update_or_create(
                    travel_info=travel,
                    transport=other_transport,
                    defaults={"custom_transport_text": other_text}
                )

            #  テンプレート作成（1つだけ）
            
            template = template_source(travel, request.user)


            # 新規作成完了 → フラグ OFF
            request.session["creating_travel"] = False
            del request.session["travel_step1"]
            messages.success(request, "テンプレートを自動作成しました")
            return redirect("app:template_edit", template_id=template.id)

        # -----------------------------
        # コピー作成（旧旅行からコピー）
        # -----------------------------
        if action == "copy":
            form = TravelStep2Form()  # 空フォーム

            old_travel_id = request.POST.get("old_travel_id")
            old_travel = get_object_or_404(Travel_info, pk=old_travel_id)
            old_template = Template.objects.filter(travel_info=old_travel).first()

            start_date = datetime.strptime(step1_data["start_date"], "%Y-%m-%d").date()
            end_date = datetime.strptime(step1_data["end_date"], "%Y-%m-%d").date()

            travel = Travel_info.objects.create(
                user=request.user,
                travel_title=step1_data["travel_title"],
                start_date=start_date,
                end_date=end_date,
                stay_type=step1_data["stay_type"],
                location=old_travel.location,
                memo=old_travel.memo,
            )

            # 交通手段コピー
            for tm in old_travel.travelmode_set.all():
                Travelmode.objects.update_or_create(
                    travel_info=travel,
                    transport=tm.transport,
                    defaults={"custom_transport_text": tm.custom_transport_text}
                )

            #  テンプレートは1つだけ
            new_template = Template.objects.create(
                travel_info=travel,
                user=request.user,
                source_type=Template.SourceType.FROM_TEMPLATE,
                template_source=old_template,
            )
            
            old_categories = TravelCategory.objects.filter(template=old_template)

            #  初回作成時だけカテゴリ・アイテムをコピー
            for old_cat in old_categories:
                new_cat = TravelCategory.objects.create(
                    template=new_template,
                    category_name=old_cat.category_name,
                    category_color=old_cat.category_color,
                    travel_type=old_cat.travel_type,
                )

                for old_item in old_cat.travelitem_set.all():
                    TravelItem.objects.create(
                        travel_category=new_cat,
                        item_name=old_item.item_name,
                        item_checked=old_item.item_checked,
                    )

            # コピー完了 → フラグ OFF
            request.session["creating_travel"] = False

            del request.session["travel_step1"]
            return redirect("app:old_template_copy", template_id=new_template.id)

    else:
        step2_data = request.session.get("travel_step2")
        if step2_data:
            form = TravelStep2Form(initial={
               "location": step2_data.get("location", ""),
               "transport_types": step2_data.get("transport", []),
               "memo": step2_data.get("memo", ""),
            })
        else:
            form = TravelStep2Form()
    # -----------------------------
    # Home と同じステータスロジック
    # -----------------------------
    templates = Template.objects.filter(
    travel_info__user=request.user
    )
    
    today = date.today()

    completed_travel_ids = (
        TravelItem.objects
        .filter(travel_category__template__travel_info__user=request.user)
        .values("travel_category__template__travel_info")
        .annotate(
            total=Count("id"),
            done=Count("id", filter=Q(item_checked=TravelItem.ItemChecked.YES))
        )
        .filter(total=F("done"))
        .values_list("travel_category__template__travel_info", flat=True)
    )

    for t in templates:
        info = t.travel_info
        if info.end_date < today:
            t.display_status = "済"
        elif info.travel_info_id in completed_travel_ids:
            t.display_status = "完"
        else:
            t.display_status = "未"

    return render(request, "new_travel/travel_step2.html", {
        "form": form,
        "step1": step1_data,
        "templates": templates,
    })