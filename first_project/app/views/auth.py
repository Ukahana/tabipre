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


from ..forms.auth import (
    RegistForm,
    UserLoginForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
)
from django.conf import settings

# ============================
# 新規登録
# ============================
class RegistUserView(CreateView):
    template_name = 'login/regist.html'
    form_class = RegistForm
    success_url = reverse_lazy('app:home')

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return self.request.GET.get("next") or super().get_success_url()


# ============================
# ログイン
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

        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return self.request.GET.get("next") or super().get_success_url()


# ============================
# パスワード再設定（メール送信）
# ============================
class PasswordResetMailView(PasswordResetView):
    template_name = 'login/password_reset.html'
    form_class = CustomPasswordResetForm

    email_template_name = 'login/password_reset_email.txt'
    html_email_template_name = 'login/password_reset_email.html'
    subject_template_name = 'login/password_reset_subject.txt'


    def form_valid(self, form):
         # Django のメール送信処理を直接呼ぶ（URL 生成含む）
        form.save(
            request=self.request,
            use_https=self.request.is_secure(),
            email_template_name=self.email_template_name,
            html_email_template_name=self.html_email_template_name,
            subject_template_name=self.subject_template_name,
            extra_email_context={},
        )

        messages.success(self.request, "パスワード再設定メールを送信しました。")

        # リダイレクトせず同じ画面を表示
        return render(self.request, self.template_name, {
         "form": self.form_class()
        })

# ============================
# パスワード再設定（新パスワード入力）
# ============================
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'login/password_reset_link.html'
    success_url = reverse_lazy('app:password_reset_complete')
    form_class = CustomSetPasswordForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, "parts/expired.html", {
                "mode": "password_reset",
                "is_share_page": True,
            })
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        if not self.validlink:
            return render(request, "parts/expired.html", {
                "mode": "password_reset",
                "is_share_page": True,
            })
        return response


# ============================
# パスワード再設定完了
# ============================
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "パスワードの変更が完了しました。")

        next_url = request.GET.get("next")
        if next_url:
            return redirect(f"{reverse_lazy('app:login')}?next={next_url}")

        return redirect('app:login')