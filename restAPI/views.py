from django.shortcuts import render
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import alumnos
from rest_framework.decorators import api_view
from .serializers import AlumnoSerializer, ProfesorSerializer
from copy import deepcopy

# Create your views here.
class Alumno():
    def __init__(self, id, nombres, apellidos, matricula, promedio):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.matricula = matricula
        self.promedio = promedio
#Array for non db data
AlumnosArray= []

class Profesor():
    def __init__(self, id, numeroEmpleado, nombres, apellidos, horasClase):
        self.id = id
        self.numeroEmpleado = numeroEmpleado
        self.nombres = nombres
        self.apellidos = apellidos
        self.horasClase = horasClase
#Array for non db data
ProfesoresArray= []

@api_view(['GET','POST'])
def do_Alumnos(request):
    if request.method == 'GET':
        return JsonResponse(AlumnosArray, safe=False)
    if request.method == 'POST':

        serializer = AlumnoSerializer(data=request.data)
        if serializer.is_valid():
            alumno_obj = Alumno(int(request.data.get('id',0)), request.data.get('nombres',''), request.data.get('apellidos',''),request.data.get('matricula',''), float(request.data.get('promedio',0)))
            AlumnosArray.append(alumno_obj.__dict__)
            return JsonResponse(alumno_obj.__dict__, safe=False, status= status.HTTP_201_CREATED)
        else:
            return JsonResponse(["Data is incorrect, could not create object"],safe=False, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET','DELETE','PUT'])
def do_Alumno_specific(request, alumnoId):

    if request.method == 'GET':
        result_alumno= [alumno for alumno in AlumnosArray if alumno["id"]==alumnoId]
        if bool(result_alumno):
            return JsonResponse(result_alumno[0],safe=False, status= status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        result_alumno= [alumno for alumno in AlumnosArray if alumno["id"]==alumnoId]
        if bool (result_alumno):
            for i,alumno in enumerate(AlumnosArray):
                if alumno["id"] ==alumnoId:
                    AlumnosArray.pop(i)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        result_alumno= [alumno for alumno in AlumnosArray if alumno["id"]==alumnoId]
        if bool (result_alumno):
            for i,alumno in enumerate(AlumnosArray):
                if alumno["id"]== alumnoId:
                    validation_alumno =deepcopy(alumno)
                    validation_alumno.update(request.data)
                    serializer = AlumnoSerializer(data=validation_alumno)
                    if serializer.is_valid():
                        alumno.update(request.data)
                        return JsonResponse(alumno,safe=False,status=status.HTTP_200_OK)
                    else:
                        return JsonResponse(["Invalid data"],safe=False,status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET','POST'])
def do_Profesores(request):
    if request.method == 'GET':
        return JsonResponse(ProfesoresArray, safe=False)
    if request.method == 'POST':
        serializer = ProfesorSerializer(data=request.data)
        if serializer.is_valid():
            profesor_obj = Profesor(int(request.data.get('id',0)),int(request.data.get('numeroEmpleado',0)),request.data.get('nombres',''),request.data.get('apellidos',''),int(request.data.get('horasClase',0)))
            ProfesoresArray.append(profesor_obj.__dict__)
            return JsonResponse(profesor_obj.__dict__,safe=False, status= status.HTTP_201_CREATED)
        else:
            return JsonResponse(["Data is incorrect, could not create object"], safe=False, status= status.HTTP_400_BAD_REQUEST)

@api_view(['GET','DELETE','PUT'])
def do_Profesor_specific(request,profId):
    if request.method=='GET':
        result_profesor= [profesor for profesor in ProfesoresArray if profesor["id"]==profId]
        if bool(result_profesor):
            return JsonResponse(result_profesor[0], safe=False, status= status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        result_profesor= [profesor for profesor in ProfesoresArray if profesor["id"]==profId]
        if bool(result_profesor):
            for i, profesor in enumerate(ProfesoresArray):
                if profesor["id"] == profId:
                    ProfesoresArray.pop(i)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        result_profesor = [profesor for profesor in ProfesoresArray if profesor["id"]==profId]
        if bool(result_profesor):
            for i, profesor in enumerate(ProfesoresArray):
                if profesor["id"] == profId:
                    validation_profesor = deepcopy(profesor)
                    validation_profesor.update(request.data)
                    serializer = ProfesorSerializer(data=validation_profesor)
                    if serializer.is_valid():
                        profesor.update(request.data)
                        return JsonResponse(profesor, safe=False, status=status.HTTP_200_OK)
                    else:
                        return JsonResponse(["Invalid data"],safe=False, status=status.HTTP_400_BAD_REQUEST)
