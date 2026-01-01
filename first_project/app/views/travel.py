from django.shortcuts import render, redirect
from ..forms.travel import (TravelStep1Form,TravelStep2Form)


def TravelStep1View(request):
    if request.method == "POST":
        form = TravelStep1Form(request.POST)
        if form.is_valid():
            # Step2 に渡すためにセッションへ保存
            request.session['travel_step1'] = form.cleaned_data
            return redirect('travel_step2')
    else:
        form = TravelStep1Form()

    return render(request, 'travel/travel_step1.html', {'form': form})

def TravelStep2View(request):
    if request.method == "POST":
        form = TravelStep2Form(request.POST)
        if form.is_valid():
            # Step2 のデータをセッションに保存
            request.session['travel_step2'] = form.cleaned_data

    else:
        form = TravelStep2Form()

    return render(request, 'travel/travel_step2.html', {'form': form})
