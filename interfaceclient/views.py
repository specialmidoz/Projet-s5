from django.shortcuts import render, redirect
from django.shortcuts import render, redirect

from pymongo import MongoClient
from django.http import JsonResponse
from elasticsearch import Elasticsearch
import json
def interfaceclient(request):


        client = MongoClient()
        db = client['ps5']
        es = Elasticsearch()
        voitures = db.voitures.find({}, {'_id': False})
        for voiture in voitures :
            #print  voiture
            jsonarray = json.dumps(voiture)
            #print jsonarray
            res = es.index(index="projects5", doc_type='voitures', body=jsonarray)

        # print type(voitures)

        return JsonResponse({'foo':'bar'})

    # Create your views here.


        # global voitures
        # context = {}
        # context['voitures_nbr'] = db.voitures.find().count()
        # context['essence'] = db.voitures.find({"typecarburant": "Essence"}).count()
        # context['diesel'] = db.voitures.find({"typecarburant": "Diesel"}).count()
        # villes = db.voitures.find({}, {'ville': 1, '_id': 0})
        # context['villes'] = set()
        # for ville in villes:
        #     context['villes'].add(ville['ville'])
        # context['villes'] = list(context['villes'])
        # villes_final = []
        # for ville in context['villes']:
        #     l = []
        #     l.append(ville)
        #     l.append(db.voitures.find({'ville': ville}).count())
        #     villes_final.append(l)
        # context['ville'] = villes_final

        # return render(request, 'index.html', context)
        #
        #
        #
        #
        # return render(request,'interfaceclient.html')
def indexelasticsearch(request):
    client = MongoClient()
    db = client['ps5']
    es = Elasticsearch()
    es.indices.delete(index='projects5', ignore=[400, 404])
    voitures = db.voitures.find({}, {'_id': False})
    for voiture in voitures:
        jsonarray = json.dumps(voiture)
        res = es.index(index="projects5", doc_type='voitures', body=jsonarray)
    return JsonResponse({'succes_index': 'true'})

def registeruser(request):
    if request.POST:
        fullname = request.POST['fullname']
        password = request.POST['password']
        email = request.POST['email']
        ville = request.POST['ville']
        typecarburant = request.POST['typecarburant']
        modele = request.POST['modele']
        client = MongoClient()
        db = client['ps5']
        collection = db['client']
        collection.insert({'fullname':fullname, 'password': password, 'email': email, 'ville': ville, 'typecarburant':typecarburant, 'modele':modele})
        return redirect('/interfaceclient/registeruser')
    return render(request, 'registeruser.html')




def loginuser(request):
    context={}
    print 'route >> enter'
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        context['email']=email
        client = MongoClient()
        db = client['ps5']
        collection = db['client']
        if collection.find({'email':email,'password':password}).count() != 0:
            user =  collection.find_one({'email':request.POST['email']},{'_id': False})
            request.session['client'] = user
            return render(request,'vitrine.html',context)
        else:
            context['error']="Not found"
            #todo modif
            return redirect('www.facebook.com')

        return render(request,'vitrine.html',context)

    else:
        return render(request, 'registeruser.html', context)


def vitrine(request):
    return render(request, 'vitrine.html')

    # try:
    #     context = {}
    #     client = request.session.get('client')
    #     es = Elasticsearch()
    #     voitures = es.search(index='projects5', doc_type='voitures', body={'size': 10})
    #     # request.session.get('client')['ville']
    #     voitures = voitures['hits']['hits']
    #     context['voitures'] = voitures
    #     # for voiture in voitures :
    #     #     print voiture
    #     voitures_recommended = es.search(index='projects5', doc_type='voitures', body={'size': 10, "query": {
    #         "bool": {
    #             "should": [
    #                 {"match": {"ville": request.session.get('client')['ville']}},
    #
    #                 {"match": {"typecarburant": request.session.get('client')['typecarburant']}}
    #             ]
    #         }
    #     }})
    #     voitures_recommended = voitures_recommended['hits']['hits']
    #     for v in voitures_recommended:
    #         print v
    #     return render(request, 'vitrine.html',context)
    # except:
    #     return redirect('/interfaceclient/registeruser')


