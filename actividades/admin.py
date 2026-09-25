from django.contrib import admin

from .models import Actividad, DependenciaActividad


@admin.register(DependenciaActividad)
class DependenciaActividadAdmin(admin.ModelAdmin):
    list_display = (
        "actividad",
        "depende_de",
        "tipo",
        "retraso_dias",
    )

    list_filter = ("tipo",)
    search_fields = (
        "actividad__nombre",
        "depende_de__nombre",
    )


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "nombre",
        "proyecto",
        "fecha_inicio",
        "fecha_fin",
        "porcentaje_avance",
        "estado",
    )

    list_filter = (
        "estado",
        "prioridad",
        "proyecto",
    )

    search_fields = (
        "codigo",
        "nombre",
    )