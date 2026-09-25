from django.contrib import admin
from .models import CategoriaEnlace, GrupoEnlace, EnlaceInteres

@admin.register(CategoriaEnlace)
class CategoriaEnlaceAdmin(admin.ModelAdmin):
    list_display = ("nombre", "orden", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre",)

@admin.register(GrupoEnlace)
class GrupoEnlaceAdmin(admin.ModelAdmin):
    list_display = ("titulo", "categoria", "orden", "activo")
    list_filter = ("activo", "categoria")
    search_fields = ("titulo", "categoria__nombre")

@admin.register(EnlaceInteres)
class EnlaceInteresAdmin(admin.ModelAdmin):
    list_display = ("nombre", "grupo", "url", "orden", "activo")
    list_filter = ("activo", "grupo__categoria")
    search_fields = ("nombre", "descripcion", "grupo__titulo")
