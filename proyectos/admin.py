from django.contrib import admin

from .models import TipoProyecto, Proyecto


@admin.register(TipoProyecto)
class TipoProyectoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "activo",
    )

    list_filter = (
        "activo",
    )

    search_fields = (
        "nombre",
    )

    ordering = (
        "nombre",
    )


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "nombre",
        "tipo",
        "area_responsable",
        "fecha_inicio",
        "fecha_fin",
        "estado",
        "activo",
    )

    list_filter = (
        "estado",
        "tipo",
        "area_responsable",
        "activo",
    )

    search_fields = (
        "codigo",
        "nombre",
        "descripcion",
    )

    filter_horizontal = (
        "coordinadores",
    )

    date_hierarchy = "fecha_inicio"

    ordering = (
        "-fecha_inicio",
        "nombre",
    )

    readonly_fields = (
        "creado_en",
        "actualizado_en",
    )

    fieldsets = (
        (
            "Información general",
            {
                "fields": (
                    "codigo",
                    "nombre",
                    "descripcion",
                    "tipo",
                )
            },
        ),
        (
            "Responsabilidad",
            {
                "fields": (
                    "area_responsable",
                    "coordinadores",
                )
            },
        ),
        (
            "Programación",
            {
                "fields": (
                    "fecha_inicio",
                    "fecha_fin",
                    "estado",
                    "activo",
                )
            },
        ),
        (
            "Auditoría",
            {
                "fields": (
                    "creado_en",
                    "actualizado_en",
                ),
                "classes": (
                    "collapse",
                ),
            },
        ),
    )