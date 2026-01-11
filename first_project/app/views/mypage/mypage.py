from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def mypage(request):
    return render(request, 'mypage/mypage.html')