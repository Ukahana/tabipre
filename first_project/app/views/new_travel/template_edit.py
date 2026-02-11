from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ...models.template import Template, TravelCategory

def template_edit(request, template_id):
    template = get_object_or_404(Template, id=template_id, user=request.user)
    categories = TravelCategory.objects.filter(template=template)

    # ⭐ POST（保存）時に is_draft=0 に更新
    if request.method == "POST":
        template.is_draft = 0
        template.save()
        messages.success(request, "テンプレートを保存しました")
        return redirect("app:template_edit", template_id=template.id)

    # GET（編集画面表示）
    return render(request, "new_travel/template_edit.html", {
        "template": template,
        "categories": categories,
    })