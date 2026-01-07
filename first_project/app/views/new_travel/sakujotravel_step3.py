from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from app.models import Travel_info, Template, TravelCategory, TravelItem


@login_required
def OldTravelCopyView(request, travel_id):
    if request.method == "POST":
        template_id = request.POST.get("template_id")

        travel_info = get_object_or_404(Travel_info, travel_info_id=travel_id)
        source = get_object_or_404(Template, id=template_id)

        # 新しいテンプレートを作成
        new_template = Template.objects.create(
            user=request.user,
            travel_info=travel_info,
            source_type=Template.SourceType.FROM_TEMPLATE,
            template_source=source,
        )

        # カテゴリとアイテムをコピー
        for cat in source.travelcategory_set.all():
            new_cat = TravelCategory.objects.create(
                template=new_template,
                category_name=cat.category_name,
                travel_type=cat.travel_type,
                category_color=cat.category_color,
            )

            for item in cat.travelitem_set.all():
                TravelItem.objects.create(
                    travel_category=new_cat,
                    item_name=item.item_name,
                    item_checked=TravelItem.ItemChecked.NO,
                )

        messages.success(request, "テンプレートをコピーして作成しました！")
        return redirect("app:template_edit", template_id=new_template.id)

    return redirect("app:travel_detail", travel_id=travel_id)

