from django.shortcuts import render,redirect
from django.views.generic import(
    TemplateView,CreateView,FormView,View
)
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from .forms import ResistForm,UserLoginForm

class HomeView(TemplateView):
    template_name = 'home.html'
    
class RegistUserView(CreateView):
    template_name = 'regist.html'
    form_class = ResistForm
    success_url = reverse_lazy('app:home')

class UserLoginView(FormView):
    template_name = 'login/user_login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('app.home')
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user= authenticate(email=email,password=password)
        if user:
          login(self.request,user)
          return redirect(self.get_success_url())
        else:
            # ログイン失敗時
         form.add_error(None, "メールアドレスまたはパスワードが違います")
         return self.form_invalid(form)
