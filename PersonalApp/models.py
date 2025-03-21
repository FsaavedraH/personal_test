from django.db import models

# Create your models here.
class Personal(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False )
    apellido = models.CharField(max_length=100, null=False, blank=False)
    cedula = models.IntegerField(unique=True, null=False, blank=False)
    fecha_ingreso = models.DateField (null=False, blank=False)
    asistencia = models.BooleanField(null=False, blank=False)
    