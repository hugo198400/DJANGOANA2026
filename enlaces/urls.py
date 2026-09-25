from django.urls import path
from . import views

app_name = "enlaces"

urlpatterns = [
    path("", views.lista_enlaces, name="lista"),
    path("lista/", views.lista_enlaces, name="lista"),
]
