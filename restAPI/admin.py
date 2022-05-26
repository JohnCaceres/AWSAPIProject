from django.contrib import admin
from . models import alumnos, profesores, ProfesoresAdmin, AlumnosAdmin

admin.site.register(alumnos, AlumnosAdmin)
admin.site.register(profesores, ProfesoresAdmin)
# Register your models here.
