from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("clicked/", views.clicked, name="clicked"),
    path("requied-context-info/", views.get_required_context_set_to_render_template, name="clicked"),
]