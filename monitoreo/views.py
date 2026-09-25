from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import ActividadForm
from .models import Actividad, Fase, Proyecto



import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

@login_required
def proyecto_lista(request):
    """
    Lista general de proyectos.
    """

    proyectos = (
        Proyecto.objects
        .filter(activo=True)
        .select_related("coordinador_tecnico")
    )

    for proyecto in proyectos:
        actividades = proyecto.actividades.all()

        proyecto.total_actividades = actividades.count()

        proyecto.cumplidas = actividades.filter(
            estado=Actividad.Estado.CUMPLIDA
        ).count()

        proyecto.en_proceso = actividades.filter(
            estado=Actividad.Estado.EN_PROCESO
        ).count()

        proyecto.pendientes = actividades.filter(
            estado=Actividad.Estado.PENDIENTE
        ).count()

        proyecto.vencidas = actividades.filter(
            estado=Actividad.Estado.VENCIDA
        ).count()

        promedio = actividades.aggregate(
            promedio=Avg("porcentaje_avance")
        )["promedio"]

        proyecto.avance_promedio = round(
            float(promedio or 0),
            2
        )

    return render(
        request,
        "monitoreo/proyecto_lista.html",
        {
            "proyectos": proyectos,
        },
    )


@login_required
def proyecto_resumen(request, pk):
    """
    Resumen y matriz de actividades de un proyecto.
    """

    proyecto = get_object_or_404(
        Proyecto.objects.select_related(
            "coordinador_tecnico",
        ),
        pk=pk,
        activo=True,
    )

    actividades = (
        Actividad.objects
        .filter(proyecto=proyecto)
        .select_related(
            "fase",
            "responsable",
        )
        .order_by(
            "fase__orden",
            "fase__nombre",
            "orden",
            "fecha_fin",
            "nombre",
        )
    )

    # ---------------------------------------------------------
    # Filtros
    # ---------------------------------------------------------

    buscar = request.GET.get("buscar", "").strip()
    estado = request.GET.get("estado", "").strip()
    fase_id = request.GET.get("fase", "").strip()

    if buscar:
        actividades = actividades.filter(
            Q(nombre__icontains=buscar)
            | Q(descripcion__icontains=buscar)
            | Q(baselegal__icontains=buscar)
            | Q(responsable__usuario__first_name__icontains=buscar)
            | Q(responsable__usuario__last_name__icontains=buscar)
        )

    if estado:
        actividades = actividades.filter(
            estado=estado
        )

    if fase_id:
        actividades = actividades.filter(
            fase_id=fase_id
        )

     # -----------------------------
    # Actividades para los KPI
    # -----------------------------

    todas_las_actividades = list(
        proyecto.actividades.all()
    )

    total_actividades = len(todas_las_actividades)

    total_pendientes = sum(
        1
        for actividad in todas_las_actividades
        if actividad.estado == Actividad.Estado.PENDIENTE
    )

    total_en_proceso = sum(
        1
        for actividad in todas_las_actividades
        if actividad.estado == Actividad.Estado.EN_PROCESO
    )

    total_cumplidas = sum(
        1
        for actividad in todas_las_actividades
        if actividad.estado == Actividad.Estado.CUMPLIDA
    )
























    # ---------------------------------------------------------
    # Estadísticas
    # ---------------------------------------------------------

    todas = Actividad.objects.filter(
        proyecto=proyecto
    )

    total = todas.count()

    cumplidas = todas.filter(
        estado=Actividad.Estado.CUMPLIDA
    ).count()

    en_proceso = todas.filter(
        estado=Actividad.Estado.EN_PROCESO
    ).count()

    pendientes = todas.filter(
        estado=Actividad.Estado.PENDIENTE
    ).count()

    vencidas = todas.filter(
        estado=Actividad.Estado.VENCIDA
    ).count()

    suspendidas = todas.filter(
        estado=Actividad.Estado.SUSPENDIDA
    ).count()

    canceladas = todas.filter(
        estado=Actividad.Estado.CANCELADA
    ).count()

    promedio = todas.aggregate(
        promedio=Avg("porcentaje_avance")
    )["promedio"]

    avance_promedio = round(
        float(promedio or 0),
        2
    )

    # ---------------------------------------------------------
    # Actividades próximas
    # ---------------------------------------------------------

    hoy = timezone.localdate()

    proximas = (
        todas
        .filter(
            fecha_fin__isnull=False,
            fecha_fin__gte=hoy,
        )
        .exclude(
            estado=Actividad.Estado.CUMPLIDA
        )
        .select_related("fase", "responsable")
        .order_by("fecha_fin")[:5]
    )

    # ---------------------------------------------------------
    # Actividades vencidas por fecha
    # ---------------------------------------------------------

    vencidas_fecha = (
        todas
        .filter(
            fecha_fin__isnull=False,
            fecha_fin__lt=hoy,
        )
        .exclude(
            estado__in=[
                Actividad.Estado.CUMPLIDA,
                Actividad.Estado.CANCELADA,
            ]
        )
        .select_related("fase", "responsable")
        .order_by("fecha_fin")
    )

    fases = Fase.objects.filter(
        activo=True
    )

    context = {
        "proyecto": proyecto,

        "actividades": actividades,

        "fases": fases,

        "buscar": buscar,
        "estado_filtro": estado,
        "fase_filtro": fase_id,

        "hoy": hoy,



        # KPI
        "total_actividades": total_actividades,
        "total_pendientes": total_pendientes,
        "total_en_proceso": total_en_proceso,
        "total_cumplidas": total_cumplidas,
        "avance_promedio": avance_promedio,

        # estadísticas
        "total": total,
        "cumplidas": cumplidas,
        "en_proceso": en_proceso,
        "pendientes": pendientes,
        "vencidas": vencidas,
        "suspendidas": suspendidas,
        "canceladas": canceladas,
        "avance_promedio": avance_promedio,

        "proximas": proximas,
        "vencidas_fecha": vencidas_fecha,

        "estados": Actividad.Estado.choices,
    }



    
    return render(
        request,
        "monitoreo/proyecto_resumen.html",
        context,
    )


@login_required
def actividad_crear(request, proyecto_pk):
    """
    Crear una nueva actividad para un proyecto.
    """

    proyecto = get_object_or_404(
        Proyecto,
        pk=proyecto_pk,
        activo=True,
    )

    if request.method == "POST":

        form = ActividadForm(
            request.POST,
            proyecto=proyecto,
        )

        if form.is_valid():

            actividad = form.save(
                commit=False
            )

            actividad.proyecto = proyecto

            actividad.save()

            messages.success(
                request,
                "La actividad fue registrada correctamente.",
            )

            return redirect(
                "monitoreo:proyecto_resumen",
                pk=proyecto.pk,
            )

    else:

        form = ActividadForm(
            proyecto=proyecto
        )

    return render(
        request,
        "monitoreo/actividad_form.html",
        {
            "form": form,
            "proyecto": proyecto,
            "titulo": "Nueva actividad",
        },
    )


@login_required
def actividad_editar(request, pk):
    """
    Editar una actividad existente.
    """

    actividad = get_object_or_404(
        Actividad.objects.select_related(
            "proyecto"
        ),
        pk=pk,
    )

    if request.method == "POST":

        form = ActividadForm(
            request.POST,
            instance=actividad,
            proyecto=actividad.proyecto,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "La actividad fue actualizada correctamente.",
            )

            return redirect(
                "monitoreo:proyecto_resumen",
                pk=actividad.proyecto.pk,
            )

    else:

        form = ActividadForm(
            instance=actividad,
            proyecto=actividad.proyecto,
        )

    return render(
        request,
        "monitoreo/actividad_form.html",
        {
            "form": form,
            "proyecto": actividad.proyecto,
            "actividad": actividad,
            "titulo": "Editar actividad",
        },
    )


@require_POST
@login_required
def actividad_estado(request, pk):

    actividad = get_object_or_404(
        Actividad,
        pk=pk,
    )

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse(
            {
                "ok": False,
                "error": "La información enviada no tiene un formato JSON válido.",
            },
            status=400,
        )

    estado = str(data.get("estado", "")).strip()
    observaciones = data.get("observaciones", "")

    # ---------------------------------------------------------
    # Validar estado
    # ---------------------------------------------------------

    estados_validos = {
        value
        for value, label in Actividad.Estado.choices
    }

    if estado not in estados_validos:

        return JsonResponse(
            {
                "ok": False,
                "error": f"Estado no válido: {estado}",
                "estados_validos": list(estados_validos),
            },
            status=400,
        )

    # ---------------------------------------------------------
    # Actualizar
    # ---------------------------------------------------------

    actividad.estado = estado
    actividad.observaciones = observaciones

    actividad.save(
        update_fields=[
            "estado",
            "observaciones",
            "actualizado_en",
        ]
    )

    return JsonResponse(
        {
            "ok": True,
            "id": actividad.pk,
            "estado": actividad.estado,
            "estado_display": actividad.get_estado_display(),
            "observaciones": actividad.observaciones or "",
        }
    )


@login_required
@require_POST
def actividad_avance(request, pk):
    """
    Cambio rápido del porcentaje de avance.
    """

    actividad = get_object_or_404(
        Actividad,
        pk=pk,
    )

    try:
        avance = float(
            request.POST.get(
                "porcentaje_avance",
                0,
            )
        )
    except (TypeError, ValueError):
        return JsonResponse(
            {
                "ok": False,
                "error": "Porcentaje inválido.",
            },
            status=400,
        )

    if avance < 0 or avance > 100:
        return JsonResponse(
            {
                "ok": False,
                "error": "El porcentaje debe estar entre 0 y 100.",
            },
            status=400,
        )

    actividad.porcentaje_avance = avance
    actividad.save(
        update_fields=[
            "porcentaje_avance",
            "actualizado_en",
        ]
    )

    return JsonResponse(
        {
            "ok": True,
            "avance": float(
                actividad.porcentaje_avance
            ),
        }
    )