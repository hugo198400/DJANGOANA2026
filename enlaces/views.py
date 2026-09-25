from django.shortcuts import render
from .models import CategoriaEnlace


def lista_enlaces(request):
    categorias = (
        CategoriaEnlace.objects
        .filter(activo=True)
        .prefetch_related(
            "grupos__enlaces"
        )
        .order_by("orden", "nombre")
    )

    return render(
        request,
        "lista.html",
        {
            "categorias": categorias,
        }
    )