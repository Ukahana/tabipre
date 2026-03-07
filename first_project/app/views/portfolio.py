from django.views.generic import TemplateView

class PortfolioTopView(TemplateView):
    template_name = "portfolio/portfolio_top.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_share_page"] = True   
        return context