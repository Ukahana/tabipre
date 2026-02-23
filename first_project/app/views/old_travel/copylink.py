import secrets
import json
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.dateformat import DateFormat

from app.models import Link, Travel_info, Template
from app.forms import LinkForm
from ...models.template import Template, TravelCategory, TravelItem
from django.urls import reverse


# ---------------------------------------------------------
# チェック更新（閲覧のみでも編集可能でも共通）
# ---------------------------------------------------------
@require_POST
def toggle_item_checked_share(request, token, item_id):
    # 共有リンクの存在チェック
    link = get_object_or_404(Link, share_token=token)

    # 有効期限チェック（閲覧・編集どちらでも共通）
    today = timezone.now().date()
    if link.expiration_date and link.expiration_date < today:
        return JsonResponse({"success": False, "error": "expired"}, status=400)

    # 対象テンプレート
    template = link.template

    # トークンに紐づくテンプレートの item のみ更新可能
    item = get_object_or_404(
        TravelItem,
        pk=item_id,
        travel_category__template=template
    )

    # JSON 取得
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "invalid_json"}, status=400)

    checked = data.get("checked", False)

    # 更新
    item.item_checked = 1 if checked else 0
    item.save()

    return JsonResponse({"success": True})