from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'mypage/password_change.html'
    success_url = reverse_lazy('app:password_change')

    def form_valid(self, form):
        messages.success(self.request, "パスワードを変更しました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Django が自動でエラーを form.errors に入れてくれる
        messages.error(self.request, "入力内容に誤りがあります。もう一度確認してください。")
        return super().form_invalid(form)