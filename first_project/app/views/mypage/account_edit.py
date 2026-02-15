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
    CustomPasswordChangeForm,
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
                "error_message": "現在の名前と同じです。変更がありません。",
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
            "error_current": None,
            "error_new": None,
        })

    def post(self, request):
        user = request.user

        current = request.POST.get("current_email", "").strip().lower()
        new = request.POST.get("new_email", "").strip().lower()

        error_current = None
        error_new = None

        # --- 現在のメールチェック ---
        try:
            validate_email_common(current)
        except ValidationError as e:
            error_current = e.message

        if current != user.email:
            error_current = "現在のメールアドレスが正しくありません。"

        # --- 新しいメールチェック ---
        try:
            validate_email_common(new)
        except ValidationError as e:
            error_new = e.message

        if new == user.email:
            error_new = "現在のメールアドレスと同じです。変更はありません。"

        try:
            validate_email_not_used(new, user=user)
        except ValidationError as e:
            error_new = e.message

        # --- エラーがあれば戻す ---
        if error_current or error_new:
            return render(request, self.template_name, {
                "current_email": current,
                "error_current": error_current,
                "error_new": error_new,
            })

        # --- 更新処理 ---
        user.email = new
        user.save()

        messages.success(request, "メールアドレスを更新しました。")
        return redirect("app:mypage")
    
