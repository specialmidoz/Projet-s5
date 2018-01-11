#!/usr/bin/env python
# coding: utf-8

from django.shortcuts import render, redirect

from pymongo import  MongoClient

client = MongoClient()
db = client['ps5']
voitures = db['voitures']


# Create your views here.

def index(request):
    global voitures
    context={}
    context['voitures_nbr']=db.voitures.find().count()
    context['essence']= db.voitures.find({"typecarburant":"Essence"}).count()
    context['diesel'] = db.voitures.find({"typecarburant": "Diesel"}).count()
    villes = db.voitures.find({},{'ville':1,'_id':0})
    context['villes']= set()
    for ville in villes:
        context['villes'].add(ville['ville'])
    context['villes']=list(context['villes'])
    villes_final=[]
    for ville in context['villes']:
        l=[]
        l.append(ville)
        l.append(db.voitures.find({'ville':ville}).count())
        villes_final.append(l)
    context['ville'] =villes_final


    return render(request,'index.html',context)


def login(request):
    context={}
    if request.POST:
        name = request.POST['email']
        password = request.POST['password']
        context['name']=name
        if db.users.find({'email':name,'password':password}).count() != 0:

            return redirect('/dashboard/')
        else:
            context['error']="Not found"
            return render(request,'login.html',context)

    else:
        return render(request, 'login.html', context)


