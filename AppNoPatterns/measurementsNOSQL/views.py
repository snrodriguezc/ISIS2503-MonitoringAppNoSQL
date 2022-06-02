from django.http import JsonResponse
from pymongo import MongoClient
import datetime
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.parsers import JSONParser
from django.conf import settings
from bson.objectid import ObjectId

# Create your views here.

@api_view(["GET", "POST"])
def estudiantes(request):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    estudiante = db['estudiantes']
    if request.method == "GET":
        result = []
        data = estudiante.find({})
        for dto in data:
            jsonData ={
                'id': str(dto['_id']),
                "name": dto['name']
            }
            result.append(jsonData)
        client.close()
        return JsonResponse(result, safe=False)
    if request.method == 'POST':
        data = JSONParser().parse(request)
        result = estudiante.insert(data)
        respo ={
            "MongoObjectID": str(result),
            "Message": "nuevo objeto en la base de datos"
        }
        client.close()
        return JsonResponse(respo, safe=False)

@api_view(["GET"])
def estudianteDetail(request, pk):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    estudiante = db['estudiantes']
    data = estudiante.find({'_id': ObjectId(pk)})
    result = []
    for dto in data:
        jsonData ={
            'id': str(dto['_id']),
            "name": dto['name'],
        }
        result.append(jsonData)
    client.close()
    return JsonResponse(result[0], safe=False)

@api_view(["GET", "POST"])
def psicologos(request):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    psicologo = db['psicologos']
    if request.method == "GET":
        result = []
        data = psicologo.find({})
        for dto in data:
            jsonData ={
                'id': str(dto['_id']),
                "name": dto['name']
            }
            result.append(jsonData)
        client.close()
        return JsonResponse(result, safe=False)
    if request.method == 'POST':
        data = JSONParser().parse(request)
        result = psicologo.insert(data)
        respo ={
            "MongoObjectID": str(result),
            "Message": "nuevo objeto en la base de datos"
        }
        client.close()
        return JsonResponse(respo, safe=False)

@api_view(["GET"])
def psicologoDetail(request, pk):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    psicologo = db['psicologos']
    data = psicologo.find({'_id': ObjectId(pk)})
    result = []
    for dto in data:
        jsonData ={
            'id': str(dto['_id']),
            "name": dto['name'],
        }
        result.append(jsonData)
    client.close()
    return JsonResponse(result[0], safe=False)

@api_view(["GET", "POST"])
def horarios(request):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    warning = db['horarios']
    if request.method == "GET":
        result = []
        data = warning.find({})
        for dto in data:
            jsonData ={
                'id': str(dto['_id']),
                "disponible":  dto['disponible'],
                "date": dto['date']
            }
            result.append(jsonData)
        client.close()
        return JsonResponse(result, safe=False)
    if request.method == 'POST':
        data = JSONParser().parse(request)
        data['date'] = datetime.datetime.utcnow()
        result = warning.insert(data)
        respo ={
            "MongoObjectID": str(result),
            "Message": "nuevo objeto en la base de datos"
        }
        client.close()
        return JsonResponse(respo, safe=False)


@api_view(["GET"])
def horarioDetail(request, pk):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    horario = db['horarios']
    data = horario.find({'_id': ObjectId(pk)})
    result = []
    for dto in data:
        jsonData ={
                'id': str(dto['_id']),
                "date": dto['date']
            }   
        result.append(jsonData)
    client.close()
    return JsonResponse(result[0], safe=False)

@api_view(["GET", "POST"])
def citas(request):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    cita = db['citas']
    if request.method == "GET":
        result = []
        data = cita.find({})
        for dto in data:
            jsonData = {
                "id": str(dto['_id']),
                "tipo": dto['tipo'],
                #'variable': dto['variable'],
                "estudiante": dto['estudiante'],
                "psicologo": dto['psicologo'],
                "horario": dto['horario'],
            }
            result.append(jsonData)
        client.close()
        return JsonResponse(result, safe=False)
    if request.method == "POST":
        data = JSONParser().parse(request)
        result = cita.insert(data)
        respo ={
            "MongoObjectID": str(result),
            "Message": "nuevo objeto en la base de datos"
        }
        client.close()
        return JsonResponse(respo, safe=False)

@api_view(["GET", "DELETE"])
def citaDetail(request, pk):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    cita = db['citas']
    if request.method == "GET":
        result = []
        data = cita.find({'_id': ObjectId(pk)})
        for dto in data:
            jsonData = {
                "id": str(dto['_id']),
                "tipo": dto['tipo'],
                "estudiante": dto['estudiante'],
                "psicologo": dto['psicologo'],
                "horario": dto['horario'],
            }
            result.append(jsonData)
        client.close()
        return JsonResponse(result[0], safe=False)

    if request.method == "DELETE":
        result = cita.remove({"_id": ObjectId(pk)})
        respo = {
            "MongoObjectID": str(result),
            "Mensaje": "Se ha borrado una cita"
        }
        client.close()
        return JsonResponse(respo, safe=False)