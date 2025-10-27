from django.contrib import admin
from .models import Evento, Inscripcion

class InscripcionInline(admin.TabularInline):
    model = Inscripcion
    extra = 0
    readonly_fields = ('usuario', 'fecha_inscripcion')
    can_delete = True
    show_change_link = False

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = (
        'titulo', 
        'fecha', 
        'lugar', 
        'plazas_totales', 
        'plazas_disponibles', 
        'valor',
        'asistentes_inscritos',
        'dinero_recaudado'
    )
    
    list_editable = ('plazas_disponibles', 'valor') 
    
    readonly_fields = ('asistentes_inscritos', 'dinero_recaudado')
    
    list_filter = ('lugar', 'fecha')
    
    inlines = [InscripcionInline]

    def asistentes_inscritos(self, obj):
        return obj.inscripcion_set.count()
    asistentes_inscritos.short_description = 'Asistentes'

    def dinero_recaudado(self, obj):
        if obj.valor is not None and obj.valor > 0:
            return f'${obj.valor * obj.inscripcion_set.count():,.0f}'
        return 'Entrada Liberada'
    dinero_recaudado.short_description = 'Recaudación'

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('evento', 'usuario', 'fecha_inscripcion')
    list_filter = ('evento', 'fecha_inscripcion')
    search_fields = ('usuario__username', 'evento__titulo')