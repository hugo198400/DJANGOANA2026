from django.contrib import admin

from .models import (
    Responsable,
    Proyecto,
    Fase,
    Actividad,
)


@admin.register(Responsable)
class ResponsableAdmin(admin.ModelAdmin):
    list_display = (
        "nombre_completo",
        "usuario",
        "rol",
        "cargo",
        "area",
        "activo",
    )

    list_filter = (
        "rol",
        "activo",
        "area",
    )

    search_fields = (
        "usuario__username",
        "usuario__first_name",
        "usuario__last_name",
        "usuario__email",
        "cargo",
        "area",
    )

    list_editable = (
        "rol",
        "activo",
    )

    def nombre_completo(self, obj):
        return obj.usuario.get_full_name() or obj.usuario.username

    nombre_completo.short_description = "Nombre"


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "nombre",
        "coordinador_tecnico",
        "fecha_inicio",
        "fecha_fin",
        "estado",
        "activo",
    )

    list_filter = (
        "estado",
        "activo",
        "coordinador_tecnico",
    )

    search_fields = (
        "codigo",
        "nombre",
        "contratista",
        "supervisor",
        "entidad_nombre",
    )

    list_editable = (
        "estado",
        "activo",
    )

    date_hierarchy = "fecha_inicio"

    ordering = (
        "-fecha_inicio",
        "nombre",
    )


@admin.register(Fase)
class FaseAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "orden",
        "activo",
    )

    list_filter = (
        "activo",
    )

    search_fields = (
        "nombre",
        "descripcion",
    )

    list_editable = (
        "orden",
        "activo",
    )

    ordering = (
        "orden",
        "nombre",
    )


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "proyecto",
        "fase",
        "responsable",
        "fecha_inicio",
        "fecha_fin",
        "porcentaje_avance",
        "estado",
        "orden",
    )

    list_filter = (
        "estado",
        "fase",
        "responsable",
        "proyecto",
    )

    search_fields = (
        "nombre",
        "descripcion",
        "observaciones",
        "proyecto__codigo",
        "proyecto__nombre",
        "responsable__usuario__username",
        "responsable__usuario__first_name",
        "responsable__usuario__last_name",
    )

    list_editable = (
        "porcentaje_avance",
        "estado",
        "orden",
    )

    date_hierarchy = "fecha_fin"

    ordering = (
        "proyecto",
        "fase",
        "orden",
        "fecha_fin",
        "nombre",
    )

    fieldsets = (
        (
            "Información general",
            {
                "fields": (
                    "proyecto",
                    "fase",
                    "nombre",
                    "descripcion",
                    "orden",
                    "control",
                    "baselegal",
                )
            },
        ),
        (
            "Responsable y planificación",
            {
                "fields": (
                    "responsable",
                    "fecha_inicio",
                    "fecha_fin",
                )
            },
        ),
        (
            "Seguimiento",
            {
                "fields": (
                    "porcentaje_avance",
                    "estado",
                    "observaciones",
                )
            },
        ),
    )