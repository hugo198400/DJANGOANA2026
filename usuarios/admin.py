from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Area, PerfilUsuario


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "sigla",
        "activa",
    )

    list_filter = (
        "activa",
    )

    search_fields = (
        "nombre",
        "sigla",
    )

    ordering = (
        "nombre",
    )


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "usuario",
        "rol",
        "area",
        "activo",
    )

    list_filter = (
        "rol",
        "area",
        "activo",
    )

    search_fields = (
        "usuario__username",
        "usuario__first_name",
        "usuario__last_name",
        "usuario__email",
    )

    list_select_related = (
        "usuario",
        "area",
    )

    ordering = (
        "usuario__last_name",
        "usuario__first_name",
    )


admin.site.unregister(User)


@admin.register(User)
class UsuarioAdmin(UserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
    )

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
    )