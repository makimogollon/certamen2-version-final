from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.

# ------------ EVENTO ------------

class Evento(models.Model):

    titulo = models.CharField(max_length=200) 
    fecha = models.DateField()
    hora = models.TimeField()
    lugar = models.CharField(max_length=255)   
    imagen = models.ImageField(upload_to='eventos/')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    plazas_totales = models.IntegerField(default=0) 
    plazas_disponibles = models.IntegerField(default=0)

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):

        if not self.pk: 
            self.plazas_disponibles = self.plazas_totales
        super().save(*args, **kwargs)

# ------------ INSCRIPCION ------------

class Inscripcion(models.Model):

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'evento')
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"

    def __str__(self):
        return f"Inscripción de {self.usuario.username} a {self.evento.titulo}"
    
    def clean(self):

        if self.pk is None and self.evento.plazas_disponibles <= 0:
            raise ValidationError('No quedan plazas disponibles para este evento.')