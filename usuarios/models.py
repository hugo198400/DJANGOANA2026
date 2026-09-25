# usuarios/models.py

from django.conf import settings
from django.db import models


class Area(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    sigla = models.CharField(max_length=30, blank=True)

    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Área"
        verbose_name_plural = "Áreas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class PerfilUsuario(models.Model):
    class Rol(models.TextChoices):
        ADMINISTRADOR = "ADMIN", "Administrador"
        ACTUALIZADOR = "ACTUALIZADOR", "Responsable de actualización"
        MONITOR="MONITOR", "Monitor"
        COORDINADOR = "COORDINADOR", "Coordinador"
        JEFE = "JEFE", "Jefe"

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil",
    )

    area = models.ForeignKey(
        Area,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="perfiles",
    )

    rol = models.CharField(
        max_length=20,
        choices=Rol.choices,
        default=Rol.COORDINADOR,
    )

    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username