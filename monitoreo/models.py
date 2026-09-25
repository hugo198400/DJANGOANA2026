from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models


class Responsable(models.Model):

    class Rol(models.TextChoices):
        ADMINISTRADOR = "ADMIN", "Administrador"
        ACTUALIZADOR = "ACTUALIZADOR", "Responsable de actualización"
        MONITOR = "MONITOR", "Monitor"
        COORDINADOR = "COORDINADOR", "Coordinador"
        JEFE = "JEFE", "Jefe"

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil_responsable",
    )

    cargo = models.CharField(
        max_length=150,
        blank=True,
    )

    rol = models.CharField(
        max_length=20,
        choices=Rol.choices,
        default=Rol.COORDINADOR,
    )

    area = models.CharField(
        max_length=150,
        blank=True,
    )

    activo = models.BooleanField(
        default=True,
    )

    class Meta:
        verbose_name = "Responsable"
        verbose_name_plural = "Responsables"
        ordering = [
            "usuario__last_name",
            "usuario__first_name",
        ]

    def __str__(self):
        nombre = self.usuario.get_full_name()

        return nombre or self.usuario.username


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

    nombre = models.CharField(
        max_length=250,
    )

    descripcion = models.TextField(
        blank=True,
    )

    monto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    contratista = models.CharField(
        max_length=250,
        blank=True,
    )

    supervisor = models.CharField(
        max_length=250,
        blank=True,
    )

    entidad_nombre = models.CharField(
        max_length=250,
        blank=True,
    )

    coordinador_tecnico = models.ForeignKey(
        Responsable,
        on_delete=models.PROTECT,
        related_name="proyectos_coordinados",
    )

    fecha_inicio = models.DateField()

    fecha_fin = models.DateField()

    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PLANIFICADO,
    )

    activo = models.BooleanField(
        default=True,
    )

    creado_en = models.DateTimeField(
        auto_now_add=True,
    )

    actualizado_en = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = [
            "-fecha_inicio",
            "nombre",
        ]

    def clean(self):
        if (
            self.fecha_inicio
            and self.fecha_fin
            and self.fecha_inicio > self.fecha_fin
        ):
            raise ValidationError(
                "La fecha de inicio no puede ser posterior "
                "a la fecha de fin."
            )

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Fase(models.Model):

    nombre = models.CharField(
        max_length=150,
        unique=True,
    )

    descripcion = models.TextField(
        blank=True,
    )

    activo = models.BooleanField(
        default=True,
    )

    orden = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        verbose_name = "Fase"
        verbose_name_plural = "Fases"
        ordering = [
            "orden",
            "nombre",
        ]

    def __str__(self):
        return self.nombre


class Actividad(models.Model):

    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        EN_PROCESO = "EN_PROCESO", "En proceso"
        CUMPLIDA = "CUMPLIDA", "Cumplida"
        VENCIDA = "VENCIDA", "Vencida"
        SUSPENDIDA = "SUSPENDIDA", "Suspendida"
        CANCELADA = "CANCELADA", "Cancelada"


    class Control(models.TextChoices):
        Contratista="Contratista","Contratista"
        ContratistaSupervisorDPDRH="Contratista + Supervisor + DPDRH","Contratista + Supervisor + DPDRH"
        ContratistaANA="Contratista → ANA","Contratista → ANA"
        ContratistaSupervisor="Contratista → Supervisor","Contratista → Supervisor"
        DPDRH="DPDRH","DPDRH"
        DPDRHANAContratista="DPDRH / ANA → Contratista","DPDRH / ANA → Contratista"
        DPDRHContratista="DPDRH → Contratista","DPDRH → Contratista"
        DPDRHANASupervisor="DPDRH/ANA → Supervisor","DPDRH/ANA → Supervisor"
        OficinadeAdministraciónANA="Oficina de Administración (ANA)","Oficina de Administración (ANA)"
        Supervisor="Supervisor","Supervisor"
        SupervisorDPDRH = "Supervisor → DPDRH","Supervisor → DPDRH"



    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        related_name="actividades",
    )

    fase = models.ForeignKey(
        Fase,
        on_delete=models.PROTECT,
        related_name="actividades",
    )

    nombre = models.CharField(
        max_length=250,
    )

    control = models.CharField(
        max_length=50,
        choices=Control.choices,
        default=Control.Contratista,
    )

    baselegal = models.CharField(
        max_length=250, blank=True)

    descripcion = models.TextField(
        blank=True,
    )

    responsable = models.ForeignKey(
        Responsable,
        on_delete=models.PROTECT,
        related_name="actividades",
    )

    fecha_inicio = models.DateField(
        null=True,
        blank=True,
    )

    fecha_fin = models.DateField(
        null=True,
        blank=True,
    )

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

    observaciones = models.TextField(
        blank=True,
    )

    orden = models.PositiveIntegerField(
        default=0,
    )

    creado_en = models.DateTimeField(
        auto_now_add=True,
    )

    actualizado_en = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"
        ordering = [
            "proyecto",
            "fase",
            "orden",
            "fecha_fin",
            "nombre",
        ]

    def clean(self):
        if (
            self.fecha_inicio
            and self.fecha_fin
            and self.fecha_inicio > self.fecha_fin
        ):
            raise ValidationError(
                "La fecha de inicio no puede ser posterior "
                "a la fecha de fin."
            )

    def __str__(self):
        return self.nombre