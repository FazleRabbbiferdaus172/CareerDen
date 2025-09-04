from django.shortcuts import render
from latex_template_compiler import render_latex_pdf

from .models import Profile
# Create your views here.

def index(request):
    return render(request, "core/index.html")

def clicked(request):
    PROFILE = Profile.objects.get(user=request.user)
    name = PROFILE.get_full_name()
    latex = render_latex_pdf(**{'name': name})
    return render(request, "core/clicked.html", {"pdf_path": latex})