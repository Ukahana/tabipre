from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from ..models.travel import Travel_info, Transport
from django.shortcuts import render
from django.utils import timezone
from..models .template import TravelItem

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home/home.html"
    login_url = "/"  

    def get(self, request, *args, **kwargs):
        keyword = request.GET.get("keyword", "")
        transport_filter = request.GET.get("transport", "")
        sort = request.GET.get("sort", "")

        travels = Travel_info.objects.filter(user=request.user)

        if keyword:
            travels = travels.filter(travel_title__icontains=keyword)

        if transport_filter:
            travels = travels.filter(transport__transport_type=transport_filter)

        if sort == "title_asc":
            travels = travels.order_by("travel_title")
        elif sort == "title_desc":
            travels = travels.order_by("-travel_title")
        elif sort == "date_asc":
            travels = travels.order_by("start_date")
        elif sort == "date_desc":
            travels = travels.order_by("-start_date")
            
        today = timezone.now().date()
        for t in travels:
            if t.end_date < today:
                t.status = "済"
                continue

            items = TravelItem.objects.filter(
                travel_category__template__travel_info=t
            )
            total = items.count()
            done = items.filter(item_checked=TravelItem.ItemChecked.YES).count()

            if total > 0 and total == done:
                t.status = "完"
            else:
                t.status = "未"

        paginator = Paginator(travels, 5)
        page = request.GET.get("page")
        travels_page = paginator.get_page(page)

        tags = Transport.objects.all()

        return render(request, self.template_name, {
            "travels": travels_page,
            "keyword": keyword,
            "tags": tags,
            "transport_filter": transport_filter,
            "sort": sort,
        })