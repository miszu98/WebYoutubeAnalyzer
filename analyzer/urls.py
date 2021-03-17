from django.urls import path
from . import views

urlpatterns = [
    path("", views.render_page, name="render_page"),
    path("get_data/", views.get_input, name="get_input")
]