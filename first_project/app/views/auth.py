from django.shortcuts import redirect
from django.views.generic import CreateView, FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib import messages

from ..forms.auth import (
    RegistForm,
    UserLoginForm,
    CustomPasswordResetForm,
)


# ============================
#  新規登録
# ============================
class RegistUserView(CreateView):
    template_name = 'login/regist.html'
    form_class = RegistForm
    success_url = reverse_lazy('app:home')

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object, backend='app.backends.EmailBackend')
        return redirect(self.get_success_url())


# ============================
#  ログイン
# ============================
class UserLoginView(FormView):
    template_name = 'login/user_login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('app:home')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = authenticate(
            request=self.request,
            username=email,
            password=password
        )

        if not user:
            form.add_error(None, "メールアドレスまたはパスワードが違います")
            return self.form_invalid(form)

        if not user.is_active:
            form.add_error(None, "このアカウントは現在ご利用いただけません。")
            return self.form_invalid(form)

        login(self.request, user, backend='app.backends.EmailBackend')
        return redirect(self.get_success_url())


# ============================
#  パスワード再設定（メール送信）
# ============================
class PasswordResetMailView(PasswordResetView):
    template_name = 'login/password_reset.html'
    form_class = CustomPasswordResetForm
    email_template_name = 'login/password_reset_email.txt'
    html_email_template_name = 'login/password_reset_email.html'
    subject_template_name = 'login/password_reset_subject.txt'

    # 成功後は同じ画面に戻す（トースト通知が確実に見える）
    success_url = reverse_lazy('app:password_reset')

    def form_valid(self, form):
        messages.success(self.request, "パスワード再設定用のメールを送信しました。")
        return super().form_valid(form)

