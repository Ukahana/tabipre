from django.shortcuts import redirect
from django.views.generic import CreateView, FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.conf import settings

from ..forms.auth import (
    RegistForm,
    UserLoginForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm
)

from smtplib import SMTPException
from django.core.mail import BadHeaderError
from django.shortcuts import render
from django.contrib.auth.views import PasswordResetConfirmView

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
        next_url = self.request.GET.get("next")
        return next_url if next_url else super().get_success_url()


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

        # EmailBackend を使用するため username=email で認証
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

    success_url = reverse_lazy('app:password_reset')

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
        timeout_hours = settings.PASSWORD_RESET_TIMEOUT // 3600
        context["expiration_time"] = f"{timeout_hours}時間"
        return context

    def get_email_context(self, context):
        context = super().get_email_context(context)
        timeout_hours = settings.PASSWORD_RESET_TIMEOUT // 3600
        context["expiration_time"] = f"{timeout_hours}時間"
        return context



from django.shortcuts import redirect
from django.views.generic import CreateView, FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.conf import settings

from ..forms.auth import (
    RegistForm,
    UserLoginForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm
)

from smtplib import SMTPException
from django.core.mail import BadHeaderError
from django.shortcuts import render
from django.contrib.auth.views import PasswordResetConfirmView

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
        next_url = self.request.GET.get("next")
        return next_url if next_url else super().get_success_url()


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

        # EmailBackend を使用するため username=email で認証
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

    success_url = reverse_lazy('app:password_reset')

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
        timeout_hours = settings.PASSWORD_RESET_TIMEOUT // 3600
        context["expiration_time"] = f"{timeout_hours}時間"
        return context

    def get_email_context(self, context):
        context = super().get_email_context(context)
        timeout_hours = settings.PASSWORD_RESET_TIMEOUT // 3600
        context["expiration_time"] = f"{timeout_hours}時間"
        return context



# ============================
#  パスワード再設定（新パスワード入力）
# ============================
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'mypage/password_change.html'
    success_url = reverse_lazy('app:password_reset_complete')
    form_class = CustomSetPasswordForm

    def get(self, request, *args, **kwargs):
        # Django が内部で validlink をセットする
        response = super().get(request, *args, **kwargs)

        # validlink が False のときは expired ページへ
        if not getattr(self, "validlink", False):
            return render(request, "parts/expired.html", {
                "mode": "password_reset",
                "is_share_page": True,
            })

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reset_mode'] = True
        context['is_share_page'] = True
        return context

# ============================
#  パスワード再設定完了
# ============================
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "パスワードの変更が完了しました。")
        return redirect('app:login')
    

