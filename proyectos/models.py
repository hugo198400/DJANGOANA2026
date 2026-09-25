# proyectos/models.py

from django.conf import settings
from django.db import models

from usuarios.models import Area


class TipoProyecto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Tipo de proyecto"
        verbose_name_plural = "Tipos de proyecto"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre



class Proyecto(models.Model):

    class Estado(models.TextChoices):
        PLANIFICADO = "PLANIFICADO", "Planificado"
        EN_EJECUCION = "EN_EJECUCION", "En ejecución"
        SUSPENDIDO = "SUSPENDIDO", "Suspendido"
        FINALIZADO = "FINALIZADO", "Finalizado"
        CANCELADO = "CANCELADO", "Cancelado"

    codigo = models.CharField(
        max_length=50,
        unique=True,
    )

    nombre = models.CharField(max_length=250)

    descripcion = models.TextField(blank=True)

    tipo = models.ForeignKey(
        TipoProyecto,
        on_delete=models.PROTECT,
        related_name="proyectos",
    )

    area_responsable = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
        related_name="proyectos",
    )

    coordinadores = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="proyectos_coordinados",
    )

    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PLANIFICADO,
    )

    activo = models.BooleanField(default=True)

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ["-fecha_inicio", "nombre"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"