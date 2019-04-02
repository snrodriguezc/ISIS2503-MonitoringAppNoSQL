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
    criticalPlace = db['criticalPlaces']
    if request.method == "GET":
        result = []
        data = criticalPlace.find({})
        for dto in data:
            jsonData = {
                "id": str(dto['_id']),
                "place": dto['place'],
                'measurements': dto['measurements'],
            }
            result.append(jsonData)
        data = place.find({})
        for dto in data:
            jsonData = {
                "id": str(dto['_id']),
                "place": dto['place'],
                'measurements': dto['measurements'],
            }
            result.append(jsonData)
        client.close()
        return JsonResponse(result, safe=False)
    if request.method == "POST":
        data = JSONParser().parse(request)
        measurements = []
        data['measurements'] = measurements
        data['average'] = 0
        if data["critical"] == True:
            result = criticalPlace.insert(data)
        else:
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
    criticalPlace = db['criticalPlaces']
    if request.method == "GET":
        result = []
        data = criticalPlace.find({'_id': ObjectId(pk)})
        for dto in data:
            jsonData = {
                "id": str(dto['_id']),
                "place": dto['place'],
                'measurements': dto['measurements'],
            }
            result.append(jsonData)
        if result == []:
            data = place.find({'_id': ObjectId(pk)})
            for dto in data:
                jsonData = {
                    "id": str(dto['_id']),
                    "place": dto['place'],
                    'measurements': dto['measurements'],
                }
                result.append(jsonData)
        client.close()
        return JsonResponse(result[0], safe=False)

    if request.method == "POST":
        data = JSONParser().parse(request)
        average = 0
        result = []
        jsonData = {
            'value': data["value"],
            'datetime': datetime.datetime.utcnow()
        }

        for dto in criticalPlace.find({'_id': ObjectId(pk)}):
            for d in dto["measurements"]:
                if d["variable"] == data["variable"]:
                    d["values"].append(jsonData)
                    average = ((d["average"] * (len(d["values"])-1)) + data["value"]) / len(d["values"])

                    d["average"] = average
                    result = criticalPlace.update(
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
                ],
                'average': data["value"]
            }
            result = criticalPlace.update(
                {'_id': ObjectId(pk)},
                {'$push': {'measurements': jsonDataNew}}
            )
            respo = {
                "MongoObjectID": str(result),
                "Mensaje": "Se añadió una nueva medida"
            }
            client.close()
            return JsonResponse(respo, safe=False)


        for dto in place.find({'_id': ObjectId(pk)}):
            for d in dto["measurements"]:
                if d["variable"] == data["variable"]:
                    d["values"].append(jsonData)
                    #for val in d["values"]:
                    #    average = average + val["value"]
                    average = ((d["average"] * (len(d["values"]) - 1)) + data["value"]) / len(d["values"])
                    print ("este es el promedio: ", d["average"])
                    d["average"] = average
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
                ],
                'average': data["value"]
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
            "Mensaje": "Se ha borrado un lugar",
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
    criticalPlace = db['criticalPlaces']
    result = []
    placeAv = ""
    variableName = ""
    average = 0

    # Calculo de promedio
    for dto in criticalPlace.find({'_id': ObjectId(pk)}):
        for d in dto["measurements"]:
            if d["variable"] == dataReceived["variable"]:
                placeAv = dto["place"]
                average = d["average"]

    if placeAv == "":
        for dto in place.find({'_id': ObjectId(pk)}):
            for d in dto["measurements"]:
                if d["variable"] == dataReceived["variable"]:
                    placeAv = dto["place"]
                    average = d["average"]

    # Obtener nombre de la variable
    variable = db['variables']
    dataVar = variable.find({'_id': ObjectId(dataReceived["variable"])})
    for dto in dataVar:
        variableName = dto["variable"]

    jsonData = {
        "place": placeAv,
        "variable": variableName,
        "average": average
    }

    result.append(jsonData)
    client.close()
    return JsonResponse(result, safe=False)


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





    