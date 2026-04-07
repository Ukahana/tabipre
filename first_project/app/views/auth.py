from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.conf import settings
from smtplib import SMTPException
from django.core.mail import BadHeaderError

from ..forms.auth import (
    RegistForm,
    UserLoginForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
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

    def get_success_url(self):
        return self.request.GET.get("next") or super().get_success_url()


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

    def get_success_url(self):
        return self.request.GET.get("next") or super().get_success_url()


# ============================
#  パスワード再設定（メール送信）
# ============================
class PasswordResetMailView(PasswordResetView):
    template_name = 'login/password_reset.html'
    form_class = CustomPasswordResetForm

    email_template_name = 'login/password_reset_email.txt'
    html_email_template_name = 'login/password_reset_email.html'
    subject_template_name = 'login/password_reset_subject.txt'

    success_url = reverse_lazy('app:password_reset')

    def dispatch(self, request, *args, **kwargs):
        self.next_url = request.GET.get("next") or request.POST.get("next")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, "再設定のメールを送信しました。")
            return response
        except (BadHeaderError, SMTPException, ConnectionError):
            messages.error(self.request, "メールの送信に失敗しました。時間をおいて再度お試しください。")
            return redirect('app:password_reset')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["protocol"] = self.request.scheme
        context["domain"] = self.request.get_host()

        timeout_hours = settings.PASSWORD_RESET_TIMEOUT // 3600
        context["expiration_time"] = f"{timeout_hours}時間"

        context["next"] = self.next_url

        return context

# ============================
#  パスワード再設定（新パスワード入力）
# ============================
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'login/password_reset_link.html'
    success_url = reverse_lazy('app:password_reset_complete')
    form_class = CustomSetPasswordForm

    def get(self, request, *args, **kwargs):
        # すでにログインしている場合は無効リンク扱いにする
        if request.user.is_authenticated:
            return render(request, "parts/expired.html", {
                "mode": "password_reset",
                "is_share_page": True,
            })

        response = super().get(request, *args, **kwargs)

        # トークン無効
        if not self.validlink:
            return render(request, "parts/expired.html", {
                "mode": "password_reset",
                "is_share_page": True,
            })

        # トークン有効
        context = self.get_context_data()
        context["is_share_page"] = True
        return render(request, self.template_name, context)


# ============================
#  パスワード再設定完了
# ============================
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "パスワードの変更が完了しました。")

        next_url = request.GET.get("next")
        if next_url:
            return redirect(f"{reverse_lazy('app:login')}?next={next_url}")

        return redirect('app:login')