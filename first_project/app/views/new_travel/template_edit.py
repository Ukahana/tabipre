from django.shortcuts import render, get_object_or_404
from ...models.template import Template, TravelCategory

def template_edit(request, template_id):
    template = get_object_or_404(Template, id=template_id)
    categories = TravelCategory.objects.filter(template=template)

    return render(request, "new_travel/template_edit.html", {
        "template": template,
        "categories": categories,
    })