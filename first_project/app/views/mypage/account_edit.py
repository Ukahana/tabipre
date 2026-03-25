from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError

from ...forms.auth import (
    validate_user_name_common,
    validate_email_common,
    validate_email_not_used,
)

@method_decorator(login_required, name='dispatch')
class AccountEditView(View):
    template_name = 'mypage/name_change.html'

    def get(self, request):
        return render(request, self.template_name, {
            "current_name": request.user.user_name,
            "error_message": None,
        })

    def post(self, request):
        user = request.user
        new_name = request.POST.get("user_name", "").strip()

        # --- バリデーション ---
        try:
            validate_user_name_common(new_name)
        except ValidationError as e:
            return render(request, self.template_name, {
                "current_name": new_name,
                "error_message": e.message,
            })

        if new_name == user.user_name:
            return render(request, self.template_name, {
                "current_name": new_name,
                "error_message": "同じ名前です。\n別の名前を入力してください。",
            })

        # --- 更新処理 ---
        user.user_name = new_name
        user.save()

        messages.success(request, "アカウント名を変更しました。")
        return redirect('app:mypage')

@method_decorator(login_required, name='dispatch')
class EmailChangeView(View):
    template_name = 'mypage/email_change.html'

    def get(self, request):
        return render(request, self.template_name, {
            "current_email": request.user.email,
            "error_new": None,
        })

    def post(self, request):
        user = request.user

        new = request.POST.get("new_email", "").strip().lower()
        error_new = None

        # --- メールアドレスチェック ---
        try:
            validate_email_common(new)
        except ValidationError as e:
            error_new = e.message

        if new == user.email:
            error_new = "同じメールアドレスです。\n別のメールアドレスを入力してください。"

        try:
            validate_email_not_used(new, user=user)
        except ValidationError as e:
            error_new = e.message

        # --- エラーがあれば戻す ---
        if error_new:
            return render(request, self.template_name, {
                "current_email": user.email,
                "error_new": error_new,
            })

        # --- 更新処理 ---
        user.email = new
        user.save()

        messages.success(request, "メールアドレスを更新しました。")
        return redirect("app:mypage")