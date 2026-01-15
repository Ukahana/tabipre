import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.utils.dateformat import DateFormat


from app.models import Link


# ① 共有リンク一覧画面
@login_required
def share_settings(request):
    links = Link.objects.filter(user=request.user).order_by('-created_at')

    # 日付を整形して新しい属性として追加
    for link in links:
        if link.expiration_date:
            df = DateFormat(link.expiration_date)
            link.formatted_expiration = df.format('Y.n.j')  # 例: 2026.5.1

    return render(request, 'mypage/link_list.html', {
        'links': links
    })


# ② 権限変更（モーダルの「登録」ボタン）
@login_required
@require_POST
def update_share_link(request, link_id):
    link = get_object_or_404(Link, id=link_id, user=request.user)

    data = json.loads(request.body)
    permission_type = data.get("permission")

    # 0 or 1 のときだけ更新
    if permission_type in ["0", "1"]:
        link.permission_type = int(permission_type)
        link.save()

    return JsonResponse({"status": "ok"})


# ③ リンク削除（モーダルの「リンクを削除」）
@login_required
@require_POST
def delete_share_link(request, link_id):
    link = get_object_or_404(Link, id=link_id, user=request.user)
    link.delete()
    return redirect('app:share_settings')
