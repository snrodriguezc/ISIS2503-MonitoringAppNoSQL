from django.http import JsonResponse
from pymongo import MongoClient
import datetime
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.parsers import JSONParser
from django.conf import settings
from bson.objectid import ObjectId

# Create your views here.

@api_view(["GET", "POST"])
def variables(request):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    variables = db['variables']
    if request.method == "GET":
        result = []
        data = variables.find({})
        for dto in data:
            jsonData = {
                'id': str(dto['_id']),
                "variable": dto['variable'],
                'threshold': dto['threshold']
            }
            result.append(jsonData)
        client.close()
        return JsonResponse(result, safe=False)
    
    if request.method == 'POST':
        data = JSONParser().parse(request)
        result = variables.insert(data)
        respo ={
            "MongoObjectID": str(result),
            "Message": "nuevo objeto en la base de datos"
        }
        client.close()
        return JsonResponse(respo, safe=False)

@api_view(["GET", "POST"])
def variablesDetail(request, pk):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    variables = db['variables']
    if request.method == "GET":
        data = variables.find({'_id': ObjectId(pk)})
        result = []
        for dto in data:
            jsonData ={
                'id': str(dto['_id']),
                "variable": dto['variable'],
                'threshold': dto['threshold']
            }
            result.append(jsonData)
        client.close()
        return JsonResponse(result[0], safe=False)
    if request.method == "POST":
        data = JSONParser().parse(request)
        result = variables.update(
            {'_id': ObjectId(pk)},
            {'$push': {'threshold': data}}
        )
        respo ={
            "MongoObjectID": str(result),
            "Message": "nuevo objeto en la base de datos"
        }
        return JsonResponse(respo, safe=False)

        
          
@api_view(["GET", "POST"])
def places(request):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    place = db['places']
    if request.method == "GET":
        result = []
        data = place.find({})
        for dto in data:
            jsonData = {
                "id": str(dto['_id']),
                "place": dto['place'],
                #'variable': dto['variable'],
                'measurements': dto['measurements'],
            }
            result.append(jsonData)
        client.close()
        return JsonResponse(result, safe=False)
    if request.method == "POST":
        data = JSONParser().parse(request)
        measurements = []
        data['measurements'] = measurements
        result = place.insert(data)
        respo ={
            "MongoObjectID": str(result),
            "Message": "nuevo objeto en la base de datos"
        }
        client.close()
        return JsonResponse(respo, safe=False)

@api_view(["GET", "POST", "DELETE"])
def placeDetail(request, pk):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    place = db['places']
    if request.method == "GET":
        result = []
        data = place.find({'_id': ObjectId(pk)})
        for dto in data:
            jsonData = {
                "id": str(dto['_id']),
                "place": dto['place'],
                #'variable': dto['variable'],
                'measurements': dto['measurements'],
            }
            result.append(jsonData)
        client.close()
        return JsonResponse(result[0], safe=False)
    if request.method == "POST":
        data = JSONParser().parse(request)

        jsonData = {
            'value': data["value"],
            'datetime': datetime.datetime.utcnow()
        }

        placePost = place.find({'_id': ObjectId(pk)})
        for dto in placePost:
            for d in dto["measurements"]:
                if d["variable"] == data["variable"]:
                    d["values"].append(jsonData)
                    result = place.update(
                        {'_id': ObjectId(pk)},
                        {'$set': {'measurements': dto["measurements"]}}
                    )
                    respo = {
                        "MongoObjectID": str(result),
                        "Mensaje": "Se añadió una nueva medida"
                    }
                    client.close()
                    return JsonResponse(respo, safe=False)

        jsonDataNew = {
            'variable': data["variable"],
            'values': [
                jsonData
            ]
        }
        result = place.update(
        {'_id': ObjectId(pk)},
        {'$push': {'measurements': jsonDataNew}}
        )
        respo = {
            "MongoObjectID": str(result),
            "Mensaje": "Se añadió una nueva medida"
        }
        client.close()
        return JsonResponse(respo, safe=False)

    if request.method == "DELETE":
        result = place.remove({"_id": ObjectId(pk)})
        respo = {
            "MongoObjectID": str(result),
            "Mensaje": "Se ha borrado un lugar"
        }
        client.close()
        return JsonResponse(respo, safe=False)

@api_view(["GET", "POST"])
def warnings(request):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    warning = db['warnings']
    if request.method == "GET":
        result = []
        data = warning.find({})
        for dto in data:
            jsonData ={
                "place": dto['place'],
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
def warningDetail(request, pk):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    warning = db['warnings']
    data = warning.find({'_id': ObjectId(pk)})
    result = []
    for dto in data:
        jsonData ={
            "place": dto['place'],
            "date": dto['date']
        }
        result.append(jsonData)
    client.close()
    return JsonResponse(result[0], safe=False)

@api_view(["POST"])
def average(request, pk):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    dataReceived = JSONParser().parse(request)
    place = db['places']
    data = place.find({'_id': ObjectId(pk)})
    result = []
    variableName = ""

    # Obtener nombre de la variable
    variable = db['variables']
    dataVar = variable.find({'_id': ObjectId(dataReceived["variable"])})
    for dto in dataVar:
        variableName = dto["variable"]

    # Calculo de promedio
    average = 0
    for dto in data:
        place = dto["place"]
        for val in dto["measurements"]:
            if val["variable"] == dataReceived["variable"]:
                for value in val["values"]:
                    average = average + value["value"]
                average = average / len(val["values"])

                jsonData = {
                    "place": place,
                    "variable": variableName,
                    "average": average
                }
                result.append(jsonData)
                client.close()
                return JsonResponse(result[0], safe=False)

    client.close()
    return JsonResponse(result[0], safe=False)


@api_view(["POST"])
def warningsFilter(request):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    warning = db['warnings']

    if request.method == "POST":
        data = JSONParser().parse(request)
        start = datetime.datetime.strptime(data["startDate"], '%Y-%m-%d %H:%M:%S')
        end = datetime.datetime.strptime(data["endDate"], '%Y-%m-%d %H:%M:%S')
        result = []
        data = warning.find({'date': {'$lt': end, '$gte': start}})
        for dto in data:
            jsonData = {
                "place": dto['place'],
                "date": dto['date']
            }
            result.append(jsonData)
        client.close()
        return JsonResponse(result, safe=False)





    