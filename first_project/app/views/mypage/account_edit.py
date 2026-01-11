from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages

@method_decorator(login_required, name='dispatch')
class AccountEditView(View):
    template_name = 'mypage/account_edit.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user = request.user

        # 入力値を取得
        current_email = request.POST.get("current_email")
        new_name = request.POST.get("user_name")
        new_email = request.POST.get("new_email")

        # ① 現在のメールアドレスが一致するかチェック
        if current_email != user.email:
            messages.error(request, "現在のメールアドレスが正しくありません。")
            return render(request, self.template_name)

        # ② ユーザーネームが空の場合
        if not new_name:
            messages.error(request, "名前 / ニックネームを入力してください。")
            return render(request, self.template_name)

        # ③ メールアドレスが空の場合（変更したいなら必須）
        if new_email == "":
            messages.error(request, "新しいメールアドレスを入力してください。")
            return render(request, self.template_name)

        # ④ メールアドレスが既に使われていないかチェック
        if new_email and new_email != user.email:
            from app.models import User
            if User.objects.filter(email=new_email).exists():
                messages.error(request, "このメールアドレスは既に使用されています。")
                return render(request, self.template_name)

        # ⑤ 更新処理
        user.user_name = new_name
        if new_email:
            user.email = new_email

        user.save()
        messages.success(request, "アカウント情報を更新しました。")

        return redirect('app:account_edit')