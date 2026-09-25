from django.db import models

class CategoriaEnlace(models.Model):
    nombre = models.CharField("Nivel 0", max_length=150)
    descripcion = models.TextField(blank=True)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden", "nombre"]
        verbose_name = "Categoría de enlaces"
        verbose_name_plural = "Categorías de enlaces"

    def __str__(self):
        return self.nombre


class GrupoEnlace(models.Model):
    categoria = models.ForeignKey(
        CategoriaEnlace,
        on_delete=models.CASCADE,
        related_name="grupos",
        verbose_name="Nivel 0"
    )
    titulo = models.CharField("Nivel 1", max_length=200)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden", "titulo"]
        verbose_name = "Grupo de enlaces"
        verbose_name_plural = "Grupos de enlaces"

    def __str__(self):
        return f"{self.categoria} / {self.titulo}"


class EnlaceInteres(models.Model):
    grupo = models.ForeignKey(
        GrupoEnlace,
        on_delete=models.CASCADE,
        related_name="enlaces",
        verbose_name="Nivel 1"
    )
    nombre = models.CharField(max_length=250)
    descripcion = models.TextField(blank=True)
    url = models.URLField("Enlace")
    observaciones = models.TextField(blank=True)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden", "nombre"]
        verbose_name = "Enlace de interés"
        verbose_name_plural = "Enlaces de interés"

    def __str__(self):
        return self.nombre
