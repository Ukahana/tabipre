from django.shortcuts import render, redirect, get_object_or_404
from app.models import Travel_info


# モーダル表示：過去の旅行一覧を表示するだけ
def TravelCopyModalView(request):
    past_travels = Travel_info.objects.all().order_by('-start_date')

    return render(request, "new_travel/copy_modal.html", {
        "past_travels": past_travels
    })


# コピー適用：選択した旅行の内容を Step2 のセッションへ反映
def TravelCopyApplyView(request, travel_id):
    # travel_id が存在しない場合は 404
    travel = get_object_or_404(Travel_info, id=travel_id)

    # Step2 のセッションにコピー内容を入れる
    request.session['travel_step2'] = {
        "location": travel.location,
        "transport": list(travel.transport.values_list('id', flat=True)),
        "transport_other": travel.transport_other or "",
        "memo": travel.memo or "",
    }

    # Step2 画面へ戻る
    return redirect('travel_step2')