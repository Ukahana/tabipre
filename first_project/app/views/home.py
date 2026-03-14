from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Case, When, IntegerField, Value, CharField, Count, Q, F

from ..models.travel import Travel_info, Transport
from ..models.template import TravelItem, Template


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home/home.html"
    login_url = "/"

    def get(self, request, *args, **kwargs):

        #  新規旅行作成中に離脱した場合の破棄処理
        if request.session.get("creating_travel"):
            Template.objects.filter(
                travel_info__isnull=True,
                user=request.user
            ).delete()
            request.session["creating_travel"] = False

        keyword = request.GET.get("keyword", "")
        travel_type = request.GET.getlist("travel_type")
        transport_filter = [t for t in request.GET.getlist("transport") if t]
        sort = request.GET.get("sort", "")

        travels = Travel_info.objects.filter(
            user=request.user
        )

        if keyword:
            travels = travels.filter(travel_title__icontains=keyword)

        if travel_type:
            travels = travels.filter(location__in=travel_type)

        if transport_filter:
            travels = travels.filter(
                transport__transport_type__in=transport_filter
            )

        travels = travels.distinct()

        today = timezone.now().date()

        completed_travel_ids = (
            TravelItem.objects
            .filter(travel_category__template__travel_info__user=request.user)
            .values("travel_category__template__travel_info")
            .annotate(
                total=Count("id"),
                done=Count("id", filter=Q(item_checked=1))
            )
            .filter(total=F("done"))
            .values_list("travel_category__template__travel_info", flat=True)
        )

        travels = travels.annotate(
            display_status=Case(
                When(end_date__lt=today, then=Value("済")),
                When(travel_info_id__in=completed_travel_ids, then=Value("完")),
                default=Value("未"),
                output_field=CharField()
            )
        )

        travels = travels.annotate(
            status_order=Case(
                When(display_status="完", then=0),
                When(display_status="未", then=1),
                When(display_status="済", then=2),
                default=3,
                output_field=IntegerField(),
            )
        )

        if sort == "title_asc":
            travels = travels.order_by("travel_title")
        elif sort == "title_desc":
            travels = travels.order_by("-travel_title")
        elif sort == "date_asc":
            travels = travels.order_by("start_date")
        elif sort == "date_desc":
            travels = travels.order_by("-start_date")
        else:
            travels = travels.order_by("status_order", "-start_date")

        paginator = Paginator(travels, 5)
        page = request.GET.get("page")
        travels_page = paginator.get_page(page)

        tags = Transport.objects.exclude(
            transport_type=Transport.TransportType.OTHER
        )

        return render(request, self.template_name, {
            "travels": travels_page,
            "keyword": keyword,
            "tags": tags,
            "travel_type": travel_type,
            "transport": transport_filter,
            "sort": sort,
        })