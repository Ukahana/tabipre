from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.dateformat import DateFormat
from django.urls import reverse
from django.http import HttpResponseForbidden

from app.models import Link
from ...models.template import TravelCategory, TravelItem
from django.contrib.auth.decorators import login_required
from app.forms.template_add import CategoryItemForm

def share_view(request, token):

    # ① 削除済みチェック（リンクが存在しない）
    link = Link.objects.filter(share_token=token).first()
    if not link:
        return render(request, "parts/expired.html", {
            "is_share_page": True,
        })

    # ② 期限切れチェック（削除と同じ文言で統一）
    today = timezone.now().date()
    if link.expiration_date and link.expiration_date < today:
        return render(request, "parts/expired.html", {
            "is_share_page": True,
        })

    # ③ 編集可能でも mode=view 以外なら編集画面へ
    if link.permission_type == Link.PermissionType.EDITABLE and request.GET.get("mode") != "view":
        return redirect(reverse("app:share_edit_view", args=[token]))

    # --- 閲覧専用処理 ---
    template = link.template
    travel_info = template.travel_info
    categories = TravelCategory.objects.filter(template=template)

    for cat in categories:
        cat.items = cat.travelitem_set.order_by("item_checked", "id")
        cat.checked_count_display = cat.checked_count
        cat.total_count_display = cat.total_count

    items = TravelItem.objects.filter(travel_category__template=template)
    total_items = items.count()
    checked_items = items.filter(item_checked=1).count()

    if travel_info.end_date < today:
        status = "済"
    elif total_items > 0 and total_items == checked_items:
        status = "完"
    else:
        status = "未"

    travel_info.status_label = status

    formatted_expiration = DateFormat(link.expiration_date).format("Y.n.j")

    return render(request, "old_travel/travel_detail.html", {
        "travel_info": travel_info,
        "categories": categories,
        "template": template,
        "total_items": total_items,
        "checked_items": checked_items,
        "can_check": True,
        "can_edit": False,
        "is_share_page": True,
        "formatted_expiration": formatted_expiration,
        "token": token,
        "permission_type": link.permission_type,
    })
    
@login_required
def share_edit_view(request, token):
    link = get_object_or_404(Link, share_token=token)

    if link.permission_type != Link.PermissionType.EDITABLE:
        return HttpResponseForbidden("編集権限がありません")

    template = link.template
    categories = TravelCategory.objects.filter(template=template)

    # --- GET：編集画面表示 ---
    if request.method == "GET":
        return render(request, "new_travel/template_edit2.html", {
            "current_template": template,
            "categories": categories,
            "card_travel_info": template.travel_info,
            "can_edit": True,
            "token": token,
            "permission_type": link.permission_type,
            "is_share_page": True,
        })

    # --- 分類追加 ---
    if "go_add" in request.POST:
        return redirect(reverse("app:share_add_category_item", args=[token]))

    # --- 名前変更 ---
    for cat in categories:
        new_cat_name = request.POST.get(f"category_name_{cat.id}")
        if new_cat_name:
            cat.category_name = new_cat_name
            cat.save()

        for item in cat.travelitem_set.all():
            new_item_name = request.POST.get(f"rename_{item.id}")
            if new_item_name:
                item.item_name = new_item_name
                item.save()

    # --- 削除処理 ---
    delete_cat_id = request.POST.get("delete_category")
    if delete_cat_id:
        TravelCategory.objects.filter(id=delete_cat_id).delete()

    delete_item_id = request.POST.get("delete_item")
    if delete_item_id:
        TravelItem.objects.filter(id=delete_item_id).delete()

    # --- 保存後は閲覧画面へ ---
    return redirect(f"/share/{token}/?mode=view")

@login_required
def share_add_category_item(request, token):
    link = get_object_or_404(Link, share_token=token)

    if link.permission_type != Link.PermissionType.EDITABLE:
        return HttpResponseForbidden("編集権限がありません")

    template = link.template

    # 過去の分類名（datalist 用）
    past_categories = TravelCategory.objects.filter(
        template=template
    ).values_list("category_name", flat=True)

    # カラー一覧
    color_map = dict(TravelCategory.CategoryColor.choices)

    if request.method == "POST":
        form = CategoryItemForm(request.POST, template=template)
        continue_flag = request.POST.get("continue")

        # バリデーション NG
        if not form.is_valid():
            return render(
                request,
                "new_travel/add_category_item.html",
                {
                    "form": form,
                    "template": template,
                    "past_categories": past_categories,
                    "color_map": color_map,
                    "open_continue_modal": False,
                    "is_share_edit": True,
                    "token": token,
                }
            )

        cd = form.cleaned_data

        # 分類作成 or 取得
        category, _ = TravelCategory.objects.get_or_create(
            template=template,
            category_name=cd["category_name"],
            defaults={
                "category_color": cd["category_color"],
                "travel_type": TravelCategory.TravelType.CUSTOM,
            }
        )

        # アイテム作成
        if cd["item_name"]:
            TravelItem.objects.create(
                travel_category=category,
                item_name=cd["item_name"],
                item_checked=0,
            )

        # 続けて追加
        if continue_flag == "1":
            return redirect("app:share_add_category_item", token)

        # 編集画面へ戻る
        if continue_flag == "2":
            return redirect("app:share_edit_view", token)

        # モーダル表示
        return render(
            request,
            "new_travel/add_category_item.html",
            {
                "form": CategoryItemForm(template=template),
                "template": template,
                "past_categories": past_categories,
                "color_map": color_map,
                "open_continue_modal": True,
                "is_share_edit": True,
                "token": token,
            }
        )

    # GET
    form = CategoryItemForm(template=template)
    return render(
        request,
        "new_travel/add_category_item.html",
        {
            "form": form,
            "template": template,
            "past_categories": past_categories,
            "color_map": color_map,
            "is_share_edit": True,
            "token": token,
        }
    )