from plotly.express import bar as plotly_bar
from plotly.io import to_html
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse

from latex_template_compiler import render_latex_pdf
from .utils.latex_service import get_required_context

from .models import Profile
from config.settings import addable_model
# Create your views here.

def index(request):
    return render(request, "core/index.html")

# Todo: remove the clicked view, url and template
def clicked(request):
    PROFILE = Profile.objects.get(user=request.user)
    name = PROFILE.get_full_name()
    latex = render_latex_pdf(**{'name': name})
    return render(request, "core/clicked.html", {"pdf_path": latex})


def latex_main(request):
    models = []
    for model in addable_model:
        m = {'field_names': [field.name for field in model._meta.fields],
             'records': model.objects.all(),
             'model_name': model._meta.model_name
             }
        models.append(m)
    required_context_set = get_required_context()
    context = {'models': models, 'required_template_context': required_context_set}
    return render(request, "core/latex_renderer.html", context)

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


def graph_data(request):
    return JsonResponse({"x": [1,2,3], "y": [4,5,6]}, safe=True)


def graph_view(request):
    bar_fig = plotly_bar({"x": [1,2,3], "y": [4,5,6]})
    fig_html = to_html(bar_fig, full_html=False)

    return HttpResponse(fig_html)
