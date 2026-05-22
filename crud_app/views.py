from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from .models import Producto, Perfil, Materia, MateriaBase, Tarea, SesionEstudio
from .forms import ProductoForm, PerfilForm, MateriaForm, TareaForm, TareaEditForm, SesionEstudioForm
from django.http import JsonResponse
from datetime import date

@login_required(login_url='login')
def lista_productos(request):
    materias = Materia.objects.filter(usuario=request.user)
    tareas = Tarea.objects.filter(usuario=request.user).order_by('fecha_programada')
    sesiones = SesionEstudio.objects.filter(usuario=request.user)
    hoy = timezone.now().date()

    total_tareas = tareas.count()
    tareas_completadas = tareas.filter(estado='completada').count()
    tareas_pendientes = tareas.exclude(estado='completada').count()
    horas_estudiadas = sesiones.aggregate(total=Sum('minutos'))['total'] or 0
    horas_estudiadas = round(horas_estudiadas / 60, 1)
    cumplimiento = 0
    if total_tareas > 0:
        cumplimiento = round((tareas_completadas * 100) / total_tareas)

    dias_estudio = list(sesiones.values_list('fecha', flat=True).distinct())
    racha = 0
    dia_actual = hoy
    while dia_actual in dias_estudio:
        racha += 1
        dia_actual = dia_actual - timedelta(days=1)

    tareas_urgentes = tareas.filter(
        estado__in=['pendiente', 'en_proceso'],
        fecha_programada__lte=hoy + timedelta(days=3)
    )[:5]
    recomendaciones = []
    for tarea in tareas_urgentes:
        faltante = float(tarea.horas_estimadas) - float(tarea.horas_estudiadas)
        if faltante > 0:
            recomendaciones.append(
                f'Vas atrasado en {tarea.materia.nombre}: dedica {round(faltante, 1)} horas a "{tarea.titulo}".'
            )
    if tareas_pendientes > 0:
        recomendaciones.append('Te conviene estudiar hoy mínimo 2 horas para mantener tu avance académico.')
    if not recomendaciones:
        recomendaciones.append('Vas bien. Mantén una sesión corta de repaso para conservar la racha.')

    contexto = {
        'materias': materias,
        'tareas': tareas[:8],
        'total_tareas': total_tareas,
        'tareas_completadas': tareas_completadas,
        'tareas_pendientes': tareas_pendientes,
        'horas_estudiadas': horas_estudiadas,
        'cumplimiento': cumplimiento,
        'racha': racha,
        'recomendaciones': recomendaciones,
    }
    return render(request, 'crud_app/lista_productos.html', contexto)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido {username}')
            return redirect('lista_productos')
        messages.error(request, 'Usuario o contraseña incorrectos')
        return redirect('login')
    return render(request, 'crud_app/login.html')


def logout_user(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente')
    return redirect('login')


def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not password1:
            messages.error(request, 'Faltan datos obligatorios')
            return redirect('register')
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe')
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, '¡Cuenta creada! Ya puedes iniciar sesión.')
        return redirect('login')

    return render(request, 'crud_app/register.html')


@login_required(login_url='login')
def perfil(request):
    perfil_usuario, creado = Perfil.objects.get_or_create(
        usuario=request.user,
        defaults={'nombre': request.user.username}
    )
    form = PerfilForm(request.POST or None, instance=perfil_usuario)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente')
            return redirect('perfil')
    return render(request, 'crud_app/perfil.html', {'form': form, 'perfil_usuario': perfil_usuario})


@login_required(login_url='login')
def materias(request):
    COLORES = {
        1: '#10B981',
        2: '#3B82F6',
        3: '#8B5CF6',
        4: '#F59E0B',
        5: '#EF4444',
        6: '#06B6D4',
        7: '#F97316',
        8: '#EC4899',
        9: '#6366F1',
    }

    mis_materias = Materia.objects.filter(usuario=request.user)
    mis_bases_ids = mis_materias.values_list('base_id', flat=True)

    carrera_sel = request.session.get('carrera_sel', 'sistemas')
    semestre_sel = request.session.get('semestre_sel')

    if request.method == 'POST':

        # FILTRAR
        if request.POST.get('action') == 'filtrar':
            carrera_sel = request.POST.get('carrera', 'sistemas')

            semestre = request.POST.get('semestre')
            semestre_sel = int(semestre) if semestre else None

            request.session['carrera_sel'] = carrera_sel
            request.session['semestre_sel'] = semestre_sel

            return redirect('materias')

        # AGREGAR MATERIA
        base_id = request.POST.get('base_id')

        if base_id:
            base = get_object_or_404(MateriaBase, pk=base_id)

            if int(base_id) not in mis_bases_ids:

                Materia.objects.create(
                    usuario=request.user,
                    base=base,
                    nombre=base.nombre,
                    codigo=base.codigo,
                    semestre=base.semestre,
                    color=COLORES.get(base.semestre, '#3B82F6'),
                )

                messages.success(
                    request,
                    f'"{base.nombre}" agregada correctamente ✅'
                )

            else:
                messages.warning(
                    request,
                    'Ya agregaste esa materia'
                )

            return redirect('materias')

    # CATÁLOGO DINÁMICO SEGÚN CARRERA
    catalogo = {}

    materias_carrera = MateriaBase.objects.filter(
        carrera=carrera_sel
    ).order_by('semestre', 'codigo')

    for m in materias_carrera:
        catalogo.setdefault(m.semestre, []).append(m)

    materias_semestre = []

    if semestre_sel:
        materias_semestre = MateriaBase.objects.filter(
            carrera=carrera_sel,
            semestre=semestre_sel
        ).order_by('codigo')

    return render(request, 'crud_app/materias.html', {
        'mis_materias': mis_materias,
        'catalogo': catalogo,
        'mis_bases_ids': list(mis_bases_ids),
        'carrera_sel': carrera_sel,
        'semestre_sel': semestre_sel,
        'materias_semestre': materias_semestre,
        'carreras': MateriaBase.CARRERAS,
        'semestres': range(1, 10),
    })


@login_required(login_url='login')
def eliminar_materia(request, pk):
    materia = get_object_or_404(Materia, pk=pk, usuario=request.user)
    if request.method == 'POST':
        materia.delete()
        messages.success(request, f'"{materia.nombre}" eliminada')
    return redirect('materias')


@login_required(login_url='login')
def tareas(request):

    tareas_list = Tarea.objects.filter(
        usuario=request.user
    ).order_by('fecha_programada')

    form = TareaForm(
        request.POST or None,
        usuario=request.user
    )

    if request.method == 'POST':

        if form.is_valid():

            tarea = form.save(commit=False)

            tarea.usuario = request.user
            tarea.estado = 'pendiente'

            tarea.save()

            messages.success(
                request,
                'Tarea creada correctamente'
            )

            return redirect('tareas')

        else:

            messages.error(
                request,
                'Revisa los campos del formulario'
            )

    return render(
        request,
        'crud_app/tareas.html',
        {
            'tareas': tareas_list,
            'form': form
        }
    )


@login_required(login_url='login')
def editar_tarea(request, pk):

    tarea = get_object_or_404(
        Tarea,
        pk=pk,
        usuario=request.user
    )

    if request.method == 'POST':

        form = TareaEditForm(
            request.POST,
            instance=tarea,
            usuario=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Cambios guardados correctamente'
            )

            return redirect('tareas')

        else:
            messages.error(
                request,
                'Error al guardar cambios'
            )

    else:

        form = TareaEditForm(
            instance=tarea,
            usuario=request.user
        )

    return render(
        request,
        'crud_app/editar_tarea.html',
        {
            'form': form,
            'tarea': tarea
        }
    )


@login_required(login_url='login')
def eliminar_tarea(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk, usuario=request.user)
    if request.method == 'POST':
        tarea.delete()
        messages.success(request, f'Tarea eliminada correctamente')
        return redirect('tareas')
    return redirect('tareas')


@login_required(login_url='login')
def iniciar_tarea(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk, usuario=request.user)
    if tarea.estado == 'pendiente':
        tarea.estado = 'en_proceso'
        tarea.save()
        messages.success(request, f'"{tarea.titulo}" está ahora en proceso 🚀')
    return redirect('tareas')


@login_required(login_url='login')
def completar_tarea(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk, usuario=request.user)
    tarea.estado = 'completada'
    tarea.horas_estudiadas = tarea.horas_estimadas
    tarea.save()
    messages.success(request, f'"{tarea.titulo}" marcada como completada ✅')
    return redirect('tareas')


@login_required(login_url='login')
def planificador(request):

    tareas = Tarea.objects.filter(
        usuario=request.user
    ).exclude(
        estado='completada'
    ).order_by(
        'creado_el'
    )

    plan = []

    for tarea in tareas:

        faltante = float(
            tarea.horas_estimadas
        ) - float(
            tarea.horas_estudiadas
        )

        if faltante < 0:
            faltante = 0

        recomendacion = "Repaso ligero"

        if faltante >= 2:
            recomendacion = "Bloque fuerte"

        elif faltante >= 1:
            recomendacion = "Bloque medio"

        plan.append({
            'tarea': tarea,
            'faltante': round(faltante, 1),
            'recomendacion': recomendacion
        })

    return render(
        request,
        'crud_app/planificador.html',
        {
            'plan': plan
        }
    )


@login_required(login_url='login')
def pomodoro(request):
    form = SesionEstudioForm(request.POST or None, usuario=request.user)
    if request.method == 'POST':
        if form.is_valid():
            sesion = form.save(commit=False)
            sesion.usuario = request.user
            sesion.save()
            # Actualizar horas_estudiadas en la tarea relacionada si existe
            materia = sesion.materia
            tarea_en_proceso = Tarea.objects.filter(
                usuario=request.user,
                materia=materia,
                estado='en_proceso'
            ).first()
            if tarea_en_proceso:
                tarea_en_proceso.horas_estudiadas = float(tarea_en_proceso.horas_estudiadas) + round(sesion.minutos / 60, 2)
                tarea_en_proceso.save()
            messages.success(request, 'Sesión de estudio guardada ✅')
            return redirect('pomodoro')
    return render(request, 'crud_app/pomodoro.html', {'form': form})


@login_required(login_url='login')
def estadisticas(request):
    sesiones = SesionEstudio.objects.filter(usuario=request.user)
    tareas = Tarea.objects.filter(usuario=request.user)

    horas_por_materia = sesiones.values('materia__nombre', 'materia__color').annotate(
        total=Sum('minutos')
    ).order_by('-total')

    tareas_por_estado = tareas.values('estado').annotate(total=Count('id'))

    total_minutos = sesiones.aggregate(total=Sum('minutos'))['total'] or 0
    total_horas = round(total_minutos / 60, 1)

    # Percentil y rango de estudio
    rango = _calcular_rango(total_horas)

    return render(request, 'crud_app/estadisticas.html', {
        'horas_por_materia': horas_por_materia,
        'tareas_por_estado': tareas_por_estado,
        'total_horas': total_horas,
        'rango': rango,
    })


def _calcular_rango(horas):
    """Rangos divertidos basados en horas totales de estudio."""
    rangos = [
        (0,   5,   0,  '😴 Dormilón académico',    'Recién arrancando... o dormiste todo el semestre.'),
        (5,   15,  10, '🐣 Pollito estudioso',      'Algo es algo. Vas dando tus primeros pasos.'),
        (15,  30,  25, '🚶 Caminante del saber',    'Ya tienes ritmo. El conocimiento te saluda.'),
        (30,  50,  40, '🔥 En llamas académico',    'El fuego está prendido. Sigue así, crack.'),
        (50,  80,  60, '⚡ Voltio intelectual',     'Velocidad de aprendizaje desbloqueada.'),
        (80,  120, 75, '🦅 Águila del estudio',     'Velas por la noche, victorias en el día.'),
        (120, 180, 88, '🧠 Cerebro en overdrive',   'Tu cerebro pide vacaciones pero tú no se las das.'),
        (180, 999, 98, '👨‍🚀 Astronauta del saber',  'Nivel élite. Eres literalmente una enciclopedia.'),
    ]
    for minimo, maximo, percentil, titulo, descripcion in rangos:
        if minimo <= horas < maximo:
            return {'titulo': titulo, 'descripcion': descripcion, 'percentil': percentil, 'horas': horas}
    return {'titulo': '👨‍🚀 Astronauta del saber', 'descripcion': 'Nivel élite.', 'percentil': 99, 'horas': horas}


# ---- Productos (legacy) ----
def crear_producto(request):
    form = ProductoForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado con éxito')
            return redirect('lista_productos')
    return render(request, 'crud_app/crear_producto.html', {'form': form})


def actualizar_producto(request, pk):
    p = get_object_or_404(Producto, pk=pk)
    form = ProductoForm(request.POST or None, instance=p)
    if form.is_valid():
        form.save()
        messages.success(request, 'Producto actualizado correctamente')
        return redirect('lista_productos')
    return render(request, 'crud_app/actualizar_producto.html', {'form': form, 'producto': p})


def eliminar_producto(request, pk):
    p = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        p.delete()
        messages.success(request, 'Producto eliminado correctamente')
        return redirect('lista_productos')
    return render(request, 'crud_app/eliminar_producto.html', {'producto': p})

@login_required(login_url='login')
def mover_tarea(request):

    if request.method == "POST":

        tarea_id = request.POST.get("id")
        fecha = request.POST.get("fecha")

        tarea = get_object_or_404(
            Tarea,
            id=tarea_id,
            usuario=request.user
        )

        tarea.fecha_programada = fecha
        tarea.save()

        return JsonResponse({
            "status": "ok"
        })

    return JsonResponse({
        "status": "error"
    })