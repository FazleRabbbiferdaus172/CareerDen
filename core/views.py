from django.shortcuts import render
from latex_template_compiler import render_latex_pdf, get_required_context

from .models import Profile
# Create your views here.

def index(request):
    return render(request, "core/index.html")

def clicked(request):
    PROFILE = Profile.objects.get(user=request.user)
    name = PROFILE.get_full_name()
    latex = render_latex_pdf(**{'name': name})
    return render(request, "core/clicked.html", {"pdf_path": latex})

def get_required_context_set_to_render_template(request):
    required_context_set = get_required_context()
    return render(request, "core/required_context_set.html", {"required_context_set": required_context_set})