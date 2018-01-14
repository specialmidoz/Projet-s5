from django.shortcuts import render

# Create your views here.
from elasticsearch import Elasticsearch
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

from django.core import serializers

@csrf_exempt
def search(request):
    es = Elasticsearch()
    searchTerm = ''
    if len(request.body)> 0 :
        body = json.loads(request.body)
        if body['searchTerm'] is None :
            searchTerm = ''
        else:
            searchTerm = body['searchTerm']
        if body['paginationStart'] is None :
            paginationStart = 0
        else:
            paginationStart = body['paginationStart']
    paginationSize = 20
    if len(searchTerm) > 1 :
        query ={
        "bool": {
            "should": [
                {"match": {"ville": searchTerm}},
                {"match": {"typecarburant": searchTerm}},
                {"match": {"titre": searchTerm}},
                {"match": {"marque": searchTerm}},
                {"match": {"description": searchTerm}}
            ]
        }
        }
    else :
        query = {
        "match_all": {}
        }
    voitures = es.search(index='projects5', doc_type='voitures', body={'size': paginationSize ,'from':paginationStart, "query": query})
    voitures = voitures['hits']['hits']
    return JsonResponse(voitures, safe=False)

@csrf_exempt
def recommendVoituresUser(request):
    es = Elasticsearch()
    # if len(request.body) > 0:
    #     body = json.loads(request.body)
    #     if body['villeUser'] is None:
    #         villeUser = ''
    #     else:
    #         villeUser = body['villeUser']
    #     if body['typecarburantUser'] is None:
    #         typecarburantUser = ''
    #     else:
    #         typecarburantUser = body['typecarburantUser']
    villeUser = 'Marrakech'
    typecarburantUser = 'Diesel'
    voitures_recommended = es.search(index='projects5', doc_type='voitures', body={'size': 10, "query": {
            "bool": {
                "should": [
                    {"match": {"ville": villeUser}},

                    {"match": {"typecarburant": typecarburantUser}}
                ]
            }
        }})
    voitures_recommended = voitures_recommended['hits']['hits']
    return JsonResponse(voitures_recommended, safe=False)

