from django.shortcuts import render
from latex_template_compiler import render_latex_pdf, get_required_context

from .models import Profile
from config.settings import addable_model
# Create your views here.

def index(request):
    models = []
    for model in addable_model:
        m = {'field_names': [field.name for field in Profile._meta.fields],
             'records': model.objects.all(),
             'model_name': model._meta.model_name
             }
        models.append(m)
    context = {'models': models}
    return render(request, "core/index.html", context)

def clicked(request):
    PROFILE = Profile.objects.get(user=request.user)
    name = PROFILE.get_full_name()
    latex = render_latex_pdf(**{'name': name})
    return render(request, "core/clicked.html", {"pdf_path": latex})

def get_required_context_set_to_render_template(request):
    required_context_set = get_required_context()
    return render(request, "core/required_context_set.html", {"required_context_set": required_context_set})