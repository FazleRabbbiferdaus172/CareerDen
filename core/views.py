from django.shortcuts import render

from latex_template_compiler import render_latex_pdf
from .utils.latex_service import get_required_context

from .models import Profile
from config.settings import addable_model
# Create your views here.

def index(request):
    models = []
    for model in addable_model:
        m = {'field_names': [field.name for field in model._meta.fields],
             'records': model.objects.all(),
             'model_name': model._meta.model_name
             }
        models.append(m)
    required_context_set = get_required_context()
    context = {'models': models, 'required_template_context': required_context_set}
    return render(request, "core/index.html", context)

def clicked(request):
    PROFILE = Profile.objects.get(user=request.user)
    name = PROFILE.get_full_name()
    latex = render_latex_pdf(**{'name': name})
    return render(request, "core/clicked.html", {"pdf_path": latex})


def render_template(request):
    context = {}
    for key in request.POST.keys():
        if key != 'csrfmiddlewaretoken':
            context[key] = request.POST[key]
    latex = render_latex_pdf(context)
    return render(request, "core/clicked.html", {"pdf_path": latex})

def get_required_context_set_to_render_template(request):
    required_context_set = get_required_context()
    return render(request, "core/required_context_set.html", {"required_template_context": required_context_set})