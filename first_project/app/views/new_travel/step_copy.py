from django.shortcuts import render, redirect, get_object_or_404
from app.models import Travel_info


# モーダル表示：過去の旅行一覧を表示するだけ
def TravelCopyModalView(request):
    past_travels = Travel_info.objects.filter(user=request.user).order_by('-start_date')

    return render(request, "new_travel/copy_modal.html", {
        "past_travels": past_travels
    })


# コピー適用：選択した旅行の内容を Step2 のセッションへ反映
def TravelCopyApplyView(request, travel_id):
    travel = get_object_or_404(Travel_info, travel_info_id=travel_id)

    # Step2 のセッションにコピー内容を入れる
    request.session['travel_step2'] = {
        "location": travel.location,
        "transport": list(travel.transport.values_list('id', flat=True)),
        "memo": travel.memo or "",
    }

    return redirect('travel_step2')