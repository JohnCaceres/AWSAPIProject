from django.db import models

# Create your models here.
class alumnos(models.Model):
    id = models.IntegerField(primary_key=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    matricula = models.CharField(max_length=50)
    promedio = models.FloatField()

    def __str__(self):
        return self.nombres

class profesores(models.Model):
    id = models.IntegerField(primary_key= True)
    numeroEmpleado = models.IntegerField()
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    horasClase = models.IntegerField()

    def __str__(self):
        return self.nombres
