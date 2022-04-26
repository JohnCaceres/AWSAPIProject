from rest_framework import serializers
from .models import alumnos, profesores

class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = alumnos
        fields = '__all__'

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = profesores
        fields = '__all__'
