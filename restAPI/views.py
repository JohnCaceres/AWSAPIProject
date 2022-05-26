from django.shortcuts import render
import os
from datetime import datetime
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import alumnos, profesores
from rest_framework.decorators import api_view
from .serializers import AlumnoSerializer,AlumnoSerializerGet, ProfesorSerializer
from copy import deepcopy
from boto3.session import Session
import boto3
from boto3.s3.transfer import S3Transfer

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
        allAlumnos = alumnos.objects.all()
        serializer = AlumnoSerializerGet(allAlumnos, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == 'POST':

        serializer = AlumnoSerializer(data=request.data)
        if serializer.is_valid():
            new_alumno = alumnos.objects.create(nombres=request.data.get('nombres',''), apellidos=request.data.get('apellidos',''), matricula=request.data.get('matricula',''), promedio=float(request.data.get('promedio',0)))
            #alumno_obj = Alumno(int(request.data.get('id',0)), request.data.get('nombres',''), request.data.get('apellidos',''),request.data.get('matricula',''), float(request.data.get('promedio',0)))
            #AlumnosArray.append(alumno_obj.__dict__)
            serializer = AlumnoSerializer(new_alumno)
            return JsonResponse(serializer.data, safe=False, status= status.HTTP_201_CREATED)
        else:
            return JsonResponse(["Data is incorrect, could not create object"],safe=False, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET','DELETE','PUT'])
def do_Alumno_specific(request, alumnoId):

    if request.method == 'GET':
        try:
            result_alumno = alumnos.objects.get(id=alumnoId)
            serializer = AlumnoSerializerGet(result_alumno)
            return JsonResponse(serializer.data,safe=False, status= status.HTTP_200_OK)
        except alumnos.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        try:
            alumnos.objects.get(id=alumnoId).delete()
            return Response(status= status.HTTP_200_OK)
        except alumnos.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        try:
            result_alumno = alumnos.objects.get(id=alumnoId)
            for x in request.data:
                setattr(result_alumno, x, request.data[x])
            test_serializer = AlumnoSerializer(data =result_alumno.__dict__)
            if test_serializer.is_valid():
                result_alumno.save()
                serializer = AlumnoSerializer(result_alumno)
                return JsonResponse(serializer.data,safe=False, status= status.HTTP_200_OK)
            else:
                return JsonResponse(["Invalid data"],safe=False,status=status.HTTP_400_BAD_REQUEST)
        except alumnos.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def do_Alumnos_Foto_Perfil(request,alumnoId):
    try:
        result_alumno = alumnos.objects.get(id=alumnoId)
        file_extension = os.path.splitext(str(request.FILES['foto']))[1]
        filename = datetime.now().strftime("%d-%m-%YT%H:%M:%S") + file_extension
        session = Session(region_name='us-east-1',
                          aws_access_key_id='ASIAX5W5OVHZNN6MG6FL',
                          aws_secret_access_key='dSsEdXqsP5lvc3mPrTiLo7PKUdF6vNIFwF5YgrWV',
                          aws_session_token ='FwoGZXIvYXdzENT//////////wEaDIW7uXZmEL6cZm4bMyLPAQw6z/fYdEuXICeKi3zGUAUpalLrbWwov0pZz0hpKpGkYwIhhopXJLLJr/4S1Man49vY/MEn6f5ApFNgTJUeD2qFAxNvVqVcEZq5/20V1ygjUpAOCziol9ZChLhbfl/8rqccjH7GuFDS3M/ed7wFFYEBTsLCQq5s3Vx6iJgd3uVvzdT/7hhKYilCSBNXrTWh0QcSFdiS+bUc1kAKAcOQSZTLk5sC4basHbmVmV4CeEmUHsiXQeIpF9sdT76wj84vwf7SYWkJP/NCmxDuSRYaQijnkL+UBjIt2GpPDvFxdAXZcIfw/cnT/eCyAoRv8+F2Tppf/8Jc5+7SuUgHMXynFy9YfQS6')

        s3 = session.resource('s3')
        s3.Bucket('uadyawslabprojectbucket').put_object(Key=filename, Body=request.FILES['foto'],ACL='public-read')
        client = session.client('s3')
        presigned_url = client.generate_presigned_url('get_object', Params={'Bucket': 'uadyawslabprojectbucket', 'Key': filename})
        setattr(result_alumno, 'fotoPerfilUrl', presigned_url)
        result_alumno.save()
        serializer = AlumnoSerializerGet(result_alumno)
        #file_url = '%s/%s/%s' % (client.meta.endpoint_url, 'uadyawslabprojectbucket', request.FILES['foto'].name)
        return JsonResponse(serializer.data, safe=False, status= status.HTTP_200_OK)
    except alumnos.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)




@api_view(['GET','POST'])
def do_Profesores(request):
    if request.method == 'GET':
        allProfesores = profesores.objects.all()
        serializer = ProfesorSerializer(allProfesores, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == 'POST':
        serializer = ProfesorSerializer(data=request.data)
        if serializer.is_valid():
            new_profe = profesores.objects.create(numeroEmpleado=int(request.data.get('numeroEmpleado',0)),nombres= request.data.get('nombres',''),apellidos=request.data.get('apellidos',''), horasClase=int(request.data.get('horasClase',0)))
            #alumno_obj = Alumno(int(request.data.get('id',0)), request.data.get('nombres',''), request.data.get('apellidos',''),request.data.get('matricula',''), float(request.data.get('promedio',0)))
            #AlumnosArray.append(alumno_obj.__dict__)
            serializer = ProfesorSerializer(new_profe)
            return JsonResponse(serializer.data, safe=False, status= status.HTTP_201_CREATED)
        else:
            return JsonResponse(["Data is incorrect, could not create object"],safe=False, status=status.HTTP_400_BAD_REQUEST)
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


        if request.method == 'GET':
            try:
                result_profesor = profesores.objects.get(id=profId)
                serializer = ProfesorSerializer(result_profesor)
                return JsonResponse(serializer.data,safe=False, status= status.HTTP_200_OK)
            except profesores.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'DELETE':
            try:
                profesores.objects.get(id=profId).delete()
                return Response(status= status.HTTP_200_OK)
            except profesores.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'PUT':
            try:
                result_profesor = profesores.objects.get(id=profId)
                for x in request.data:
                    setattr(result_profesor, x, request.data[x])
                test_serializer = ProfesorSerializer(data =result_profesor.__dict__)
                if test_serializer.is_valid():
                    result_profesor.save()
                    serializer = ProfesorSerializer(result_profesor)
                    return JsonResponse(serializer.data,safe=False, status= status.HTTP_200_OK)
                else:
                    return JsonResponse(["Invalid data"],safe=False,status=status.HTTP_400_BAD_REQUEST)
            except profesores.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
