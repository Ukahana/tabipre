from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ...models.template import TravelCategory

@login_required
def autocomplete_category(request):
    q = request.GET.get("q", "").strip()

    if not q:
        return JsonResponse([], safe=False)

    categories = (
        TravelCategory.objects
        .filter(template__user=request.user, category_name__icontains=q)
        .values_list("category_name", flat=True)
        .distinct()
    )

    return JsonResponse(list(categories), safe=False)
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ...models.template import TravelItem

@login_required
def autocomplete_item(request):
    q = request.GET.get("q", "").strip()

    if not q:
        return JsonResponse([], safe=False)

    items = (
        TravelItem.objects
        .filter(travel_category__template__user=request.user, item_name__icontains=q)
        .values_list("item_name", flat=True)
        .distinct()
    )

    return JsonResponse(list(items), safe=False)
