from django.urls import path

from . import views


app_name = "monitoreo"


urlpatterns = [

    path(
        "proyectos/",
        views.proyecto_lista,
        name="proyecto_lista",
    ),

    path(
        "proyectos/<int:pk>/",
        views.proyecto_resumen,
        name="proyecto_resumen",
    ),

    path(
        "proyectos/<int:proyecto_pk>/actividades/nueva/",
        views.actividad_crear,
        name="actividad_crear",
    ),

    path(
        "actividades/<int:pk>/editar/",
        views.actividad_editar,
        name="actividad_editar",
    ),

    path(
        "actividades/<int:pk>/estado/",
        views.actividad_estado,
        name="actividad_estado",
    ),

    path(
        "actividades/<int:pk>/avance/",
        views.actividad_avance,
        name="actividad_avance",
    ),
    path('seguimiento-ptto/', views.powerbi_seguimiento, name='powerbi_seguimiento'),




]