# actividades/models.py

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from proyectos.models import Proyecto


class TipoActividad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Prioridad(models.TextChoices):
    BAJA = "BAJA", "Baja"
    MEDIA = "MEDIA", "Media"
    ALTA = "ALTA", "Alta"
    CRITICA = "CRITICA", "Crítica"

class Actividad(models.Model):

    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        EN_PROCESO = "EN_PROCESO", "En proceso"
        CUMPLIDA = "CUMPLIDA", "Cumplida"
        VENCIDA = "VENCIDA", "Vencida"
        OBSERVADA = "OBSERVADA", "Observada"
        SUSPENDIDA = "SUSPENDIDA", "Suspendida"
        CANCELADA = "CANCELADA", "Cancelada"

    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        related_name="actividades",
    )

    codigo = models.CharField(max_length=50)

    nombre = models.CharField(max_length=250)

    descripcion = models.TextField(blank=True)

    tipo = models.ForeignKey(
        TipoActividad,
        on_delete=models.PROTECT,
        related_name="actividades",
    )

    actividad_padre = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subactividades",
    )

    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="actividades_responsables",
    )

    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    porcentaje_avance = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )

    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )

    prioridad = models.CharField(
        max_length=10,
        choices=Prioridad.choices,
        default=Prioridad.MEDIA,
    )

    es_hito = models.BooleanField(default=False)

    observaciones = models.TextField(blank=True)

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"
        ordering = ["fecha_fin", "codigo"]
        constraints = [
            models.UniqueConstraint(
                fields=["proyecto", "codigo"],
                name="codigo_unico_por_proyecto",
            )
        ]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class DependenciaActividad(models.Model):

    class TipoDependencia(models.TextChoices):
        FIN_INICIO = "FIN_INICIO", "Fin - Inicio"
        INICIO_INICIO = "INICIO_INICIO", "Inicio - Inicio"
        FIN_FIN = "FIN_FIN", "Fin - Fin"
        INICIO_FIN = "INICIO_FIN", "Inicio - Fin"

    actividad = models.ForeignKey(
        Actividad,
        on_delete=models.CASCADE,
        related_name="dependencias",
    )

    depende_de = models.ForeignKey(
        Actividad,
        on_delete=models.CASCADE,
        related_name="actividades_dependientes",
    )

    tipo = models.CharField(
        max_length=20,
        choices=TipoDependencia.choices,
        default=TipoDependencia.FIN_INICIO,
    )

    retraso_dias = models.PositiveIntegerField(
        default=0,
        verbose_name="Retraso en días",
    )

    class Meta:
        verbose_name = "Dependencia entre actividades"
        verbose_name_plural = "Dependencias entre actividades"

        constraints = [
            models.UniqueConstraint(
                fields=["actividad", "depende_de"],
                name="dependencia_unica",
            )
        ]

    def __str__(self):
        return (
            f"{self.depende_de} → {self.actividad}"
        )