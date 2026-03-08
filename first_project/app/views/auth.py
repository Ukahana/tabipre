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
from django.urls import reverse

# ============================
#  新規登録
# ============================
class RegistUserView(CreateView):
    template_name = 'login/regist.html'
    form_class = RegistForm
    success_url = reverse_lazy('app:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='app.backends.EmailBackend')
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

    def form_valid(self, form):
        # next を保存
        self.next_url = (
            self.request.GET.get("next")
            or self.request.POST.get("next")
        )

        try:
            response = super().form_valid(form)
            messages.success(self.request, "再設定のメールを送信しました。")
            return response
        except (BadHeaderError, SMTPException, ConnectionError):
            messages.error(self.request, "メールの送信に失敗しました。時間をおいて再度お試しください。")
            return redirect('app:password_reset')

    def _add_common_context(self, context):
        timeout_hours = settings.PASSWORD_RESET_TIMEOUT // 3600
        context["expiration_time"] = f"{timeout_hours}時間"
        return context

    def get_context_data(self, **kwargs):
        return self._add_common_context(super().get_context_data(**kwargs))

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):

        uid = context.get("uid")
        token = context.get("token")

        # パスワード再設定URLのパス部分
        reset_path = reverse('app:password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token,
        })

        # 完全なURLを生成
        base_url = f"{self.request.scheme}://{self.request.get_host()}{reset_path}"

        if self.next_url:
            reset_url = f"{base_url}?next={self.next_url}"
        else:
            reset_url = base_url

        # テンプレートに渡す
        context["reset_url"] = reset_url

        super().send_mail(
            subject_template_name,
            email_template_name,
            context,
            from_email,
            to_email,
            html_email_template_name=html_email_template_name,
        )

# ============================
#  パスワード再設定（新パスワード入力）
# ============================
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'mypage/password_change.html'
    success_url = reverse_lazy('app:password_reset_complete')
    form_class = CustomSetPasswordForm

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if not getattr(self, "validlink", False):
            return render(request, "parts/expired.html", {
                "mode": "password_reset",
                "is_share_page": True,
            })
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'reset_mode': True,
            'is_share_page': True,
            'next': self.request.GET.get("next"),
        })
        return context


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