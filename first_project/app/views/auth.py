from django.shortcuts import redirect
from django.views.generic import CreateView, FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib import messages
from ..forms.auth import RegistForm, UserLoginForm

class RegistUserView(CreateView):
    template_name = 'login/regist.html'
    form_class = RegistForm
    success_url = reverse_lazy('app:home')
    
    def form_valid(self, form):
        user = form.save(commit=True) 
        return super().form_valid(form)

class UserLoginView(FormView):
    template_name = 'login/user_login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('app:home')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(username=email, password=password)

        if user:
            login(self.request, user)
            return redirect(self.get_success_url())
        else:
            form.add_error(None, "メールアドレスまたはパスワードが違います")
            return self.form_invalid(form)


class PasswordResetMailView(PasswordResetView):
    template_name = 'login/password_reset.html'
    # ここから
    email_template_name = 'login/password_reset_email.html'
    subject_template_name = 'login/password_reset_subject.txt'
    success_url = reverse_lazy('app:user_login')

    def form_valid(self, form):
        # 成功時
        try:
            response = super().form_valid(form)
            messages.success(self.request, "パスワード再設定用のリンクを送信しました")
            return response
        # エラー時
        except Exception:
            messages.error(self.request, "メール送信に失敗しました。時間をおいて再度お試しください。")
            return self.form_invalid(form)
