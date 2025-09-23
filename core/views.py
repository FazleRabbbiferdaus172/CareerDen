from plotly.express import bar as plotly_bar
from plotly.io import to_html
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse

from latex_template_compiler import render_latex_pdf
from .utils.latex_service import get_required_context

from .models import Profile
from config.settings import addable_model
import json
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

    def get_model(model_name):
        for model in addable_model:
            if model._meta.model_name == model_name:
                return model
        return None

    context = {}
    for key in request.POST.keys():
        if key not in ['csrfmiddlewaretoken', 'encoding']:
            form_input_value = json.loads(request.POST[key])
            if form_input_value["type"] == "tr":
                input_datas = form_input_value["value"].split(',')
                input_model_name = None
                rec_ids = []
                for input_data in input_datas:
                    data_model_name, data_rec_id = input_data.split('#')
                    input_model_name = data_model_name.strip()
                    rec_ids.append(int(data_rec_id.strip()))
                model = get_model(input_model_name)
                model_field_type_mapping = dict([(field.name, field.is_relation) for field in model._meta.fields])
                columns_to_include = json.loads(form_input_value["cells"])
                recs = model.objects.filter(id__in=rec_ids)
                context_values = []
                for rec in recs:
                    context_value = {}
                    for col in columns_to_include:
                        column_data = getattr(rec, col)
                        if not model_field_type_mapping[col]:
                            context_value[col] = column_data
                        else:
                            context_value[col] = column_data.__str__()
                    context_values.append(context_value)
                context[key] = context_values
            else:
                context[key] = form_input_value["value"]
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
