# seguimiento/models.py

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from actividades.models import Actividad


class AvanceActividad(models.Model):

    actividad = models.ForeignKey(
        Actividad,
        on_delete=models.CASCADE,
        related_name="historial_avances",
    )

    fecha_corte = models.DateField()

    porcentaje = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )

    comentario = models.TextField(blank=True)

    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="avances_registrados",
    )

    registrado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Avance de actividad"
        verbose_name_plural = "Avances de actividades"
        ordering = ["-fecha_corte", "-registrado_en"]

    def __str__(self):
        return (
            f"{self.actividad} - "
            f"{self.porcentaje}% - "
            f"{self.fecha_corte}"
        )


class Observacion(models.Model):

    class Tipo(models.TextChoices):
        GENERAL = "GENERAL", "General"
        RETRASO = "RETRASO", "Retraso"
        RIESGO = "RIESGO", "Riesgo"
        DOCUMENTAL = "DOCUMENTAL", "Documental"
        TECNICA = "TECNICA", "Técnica"

    actividad = models.ForeignKey(
        Actividad,
        on_delete=models.CASCADE,
        related_name="observaciones_registradas",
    )

    tipo = models.CharField(
        max_length=20,
        choices=Tipo.choices,
        default=Tipo.GENERAL,
    )

    texto = models.TextField()

    fecha = models.DateField(auto_now_add=True)

    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )

    atendida = models.BooleanField(default=False)

    fecha_atencion = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Observación de {self.actividad}"