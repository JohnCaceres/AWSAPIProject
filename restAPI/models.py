from django.db import models
from django.contrib import admin

# Create your models here.
class alumnos(models.Model):
    id = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    matricula = models.CharField(max_length=50)
    promedio = models.FloatField()
    fotoPerfilUrl = models.CharField(max_length=1000)

    def __str__(self):
        return self.nombres

class profesores(models.Model):
    id = models.AutoField(primary_key= True)
    numeroEmpleado = models.IntegerField()
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    horasClase = models.IntegerField()

class AlumnosAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombres']

class ProfesoresAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombres']


    def __str__(self):
        return self.nombres
