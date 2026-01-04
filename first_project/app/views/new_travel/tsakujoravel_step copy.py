from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from app.models.travel import Travel_info, Transport, Travelmode
from app.forms.travel import TravelStep1Form, TravelStep2Form



# -----------------------------
# Step1：旅行の基本情報入力
# -----------------------------
def TravelStep1View(request):
    if request.method == "POST":
        form = TravelStep1Form(request.POST)
        if form.is_valid():
            # Step2 に渡すためにセッションへ保存
            request.session['travel_step1'] = form.cleaned_data
            return redirect('travel_step2')
    else:
        form = TravelStep1Form()

    return render(request, 'new_travel/travel_step1.html', {
        'form': form
    })


# -----------------------------
# Step2：場所分類・交通手段・メモ
# -----------------------------
def TravelStep2View(request):
    # Step1 の内容を取得（Step2 画面に表示するため）
    step1 = request.session.get('travel_step1')

    # モーダル用：過去の旅行一覧
    past_travels = Travel_info.objects.all().order_by('-start_date')

    if request.method == "POST":
        form = TravelStep2Form(request.POST)

        if form.is_valid():
            # Step2 のデータをセッションに保存（メモも含む）
            request.session['travel_step2'] = form.cleaned_data

            # どのボタンが押されたか判定
            action = request.POST.get("action")

            # テンプレート作成ボタン
            if action == "template":
                return redirect('template_create')

            # 前回の旅行からコピー
            if action == "copy":
                return redirect('travel_copy_modal')

        # バリデーション NG の場合はそのまま下へ（エラー表示）

    else:
        form = TravelStep2Form()

    return render(request, 'new_travel/travel_step2.html', {
        'form': form,
        'step1': step1,
        'past_travels': past_travels,  # モーダルで使用
    })
