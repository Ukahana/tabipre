from django.shortcuts import render

def TemplateCreateView(request):
    step1 = request.session.get('travel_step1')
    step2 = request.session.get('travel_step2')
    return render(request, "new_travel/template_create.html", {
        "step1": step1,
        "step2": step2,
    })