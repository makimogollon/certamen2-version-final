from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.db import IntegrityError
from .models import Evento, Inscripcion
from django.contrib.auth import login
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.db import transaction

# Create your views here.

def index(request):
    hoy = timezone.now().date()
    evento_destacado = Evento.objects.filter(fecha__gte=hoy).order_by('fecha').first()

    data = {
        'evento_destacado': evento_destacado
    }
    return render(request, 'core/index.html', data)

def eventos(request):
    hoy = timezone.localdate()
    eventos_lista = Evento.objects.filter(fecha__gte=hoy).order_by('fecha')
    data = {
        'eventos': eventos_lista
    }
    return render(request, 'core/eventos.html', data)

# ---------- 3. INFO DE EVENTOS ----------

def lista_eventos(request):

    eventos = Evento.objects.all().order_by('fecha')
    data = {
        'eventos': eventos
    }
    return render(request, 'core/eventos.html', data)

# ---------- 4. REGISTRAR CUENTA USUARIO ----------

def registro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Cuenta creada con éxito para {user.username}. ¡Bienvenido!')
            login(request, user)
            return redirect('eventos')
    else:
        form = UserCreationForm()

    data = {
        'form': form
    }
    return render(request, 'core/registro.html', data)


#---------- 6. INSCRIBIRSE A LOS EVENTOS ----------

@login_required 
def inscribirse(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    
    if Inscripcion.objects.filter(usuario=request.user, evento=evento).exists():
        messages.warning(request, f'Ya estás inscrito(a) en el evento: {evento.titulo}.')
        return redirect('mi_cuenta')

    if evento.plazas_disponibles <= 0:
        messages.error(request, f'Lo sentimos, no quedan plazas disponibles para {evento.titulo}.')
        return redirect('mi_cuenta')

    try:
        with transaction.atomic():
            Inscripcion.objects.create(usuario=request.user, evento=evento)
            evento.plazas_disponibles -= 1
            evento.save(update_fields=['plazas_disponibles'])

        messages.success(request, f'¡Inscripción exitosa! Te has registrado en: {evento.titulo}.')
        return redirect('mi_cuenta')
        
    except Exception as e:
        messages.error(request, f'Ocurrió un error al intentar inscribirte: {e}')
        return redirect('mi_cuenta')

#--------- 7. VER EVENTOS INSCRITOS ----------

@login_required
def mi_cuenta(request):
    inscripciones_usuario = Inscripcion.objects.filter(usuario=request.user).select_related('evento').order_by('-fecha_inscripcion')

    data = {
        'inscripciones': inscripciones_usuario
    }

    return render(request, 'core/mi_cuenta.html', data)

#--------- 7. ANULAR INSCRIPCIÓN A EVENTOS ----------

@login_required
def anular_inscripcion(request, inscripcion_id):

    inscripcion = get_object_or_404(Inscripcion, pk=inscripcion_id)

    if inscripcion.usuario != request.user:
        messages.error(request, 'No tienes permiso para anular esta inscripción.')
        return redirect('mi_cuenta') 

    evento = inscripcion.evento
    evento_titulo = evento.titulo

    inscripcion.delete() 
    evento.plazas_disponibles += 1
    evento.save()

    messages.success(request, f'Has anulado tu registro en el evento: {evento_titulo}.')
    return redirect('mi_cuenta')

@staff_member_required
def panel_admin(request):

    return render(request, 'core/panel_admin.html')
