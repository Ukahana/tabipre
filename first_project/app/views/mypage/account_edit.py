from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages

@method_decorator(login_required, name='dispatch')
class AccountEditView(View):
    template_name = 'mypage/name_change.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user = request.user

        # 入力値を取得
        new_name = request.POST.get("user_name")

        # 名前が空の場合
        if not new_name:
            messages.error(request, "名前 / ニックネームを入力してください。")
            return render(request, self.template_name)

        # 更新処理
        user.user_name = new_name
        user.save()

        messages.success(request, "アカウント名を変更しました。")
        return redirect('app:mypage')

    
    
@method_decorator(login_required, name='dispatch')
class EmailChangeView(View):
    template_name = 'mypage/email_change.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user = request.user
        
        current_email = request.POST.get("current_email")
        new_email = request.POST.get("new_email")

        # 現在のメール確認
        if current_email != user.email:
            messages.error(request, "現在のメールアドレスが正しくありません。")
            return render(request, self.template_name)

        # 新しいメール必須
        if not new_email:
            messages.error(request, "新しいメールアドレスを入力してください。")
            return render(request, self.template_name)

        # 同じメールアドレスなら更新不要
        if new_email == user.email:
            messages.info(request, "現在のメールアドレスと同じです。変更はありません。")
            return redirect('app:account_email')

        # 重複チェック
        from app.models import User
        if User.objects.filter(email=new_email).exists():
            messages.error(request, "このメールアドレスは既に使用されています。")
            return render(request, self.template_name)
        
        # 更新
        user.email = new_email
        user.save()
      
        messages.success(request, "メールアドレスを更新しました。")
        return redirect('app:mypage')
