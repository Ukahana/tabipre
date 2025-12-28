# 仮で作成
from django.contrib.auth.views import TemplateView
class HomeView(TemplateView):
    template_name = 'home.html'
    