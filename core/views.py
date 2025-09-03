from django.shortcuts import render
from latex_template_compiler import render_latex_pdf

# Create your views here.

def index(request):
    return render(request, "core/index.html")

def clicked(request):
    latex = render_latex_pdf()
    return render(request, "core/clicked.html", {"pdf_path": latex})