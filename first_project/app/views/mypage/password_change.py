from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from ...forms.auth import CustomPasswordChangeForm

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'mypage/password_change.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('app:mypage')

    def form_valid(self, form):
        messages.success(self.request, "パスワードを変更しました。")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reset_mode'] = False
        context['is_share_page'] = False
        return context