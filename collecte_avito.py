# -*- coding: cp1252 -*-

import urllib2
from bs4 import BeautifulSoup as soup
import json

from pymongo import  MongoClient
import pandas as pd
import openpyxl


client = MongoClient()
db = client['ps5']
collection  = db['voitures']


headers = { 'User-Agent' : 'Mozilla/5.0' }

link0 = "https://www.avito.ma/fr/maroc/voitures-%C3%A0_vendre?o="
data = {}
L =[]

def consult_modele(lien):
    global headers

    req = urllib2.Request(lien, None, headers)
    html = urllib2.urlopen(req)
    html = html.read()
    page_soup = soup(html,"lxml")
    try:

        modele = page_soup.find_all("h2", {"class": "font-normal fs12 no-margin ln22"})[0].text
       # d = dat.split(":")[1]
        modele =modele.split(":")[1]
        return modele


    except:
        return ""

def consult_paragraphe(lien):
    global headers

    req = urllib2.Request(lien, None, headers)
    html = urllib2.urlopen(req)
    html = html.read()
    page_soup = soup(html,"lxml")
    try:

        descriptif = page_soup.find("div", {"class": "span10"}).text
       # d = dat.split(":")[1]
        return descriptif


    except:
        return ""



def consult_kilo(lien):
    global headers

    req = urllib2.Request(lien, None, headers)
    html = urllib2.urlopen(req)
    html = html.read()
    page_soup = soup(html,"lxml")
    try:

        kilo = page_soup.find_all("h2", {"class": "font-normal fs12 no-margin ln22"})[1].text
       # d = dat.split(":")[1]
        kilo =kilo.split(":")[1]
        return kilo


    except:
        return ""
def consult_typecarburant(lien):
    global headers

    req = urllib2.Request(lien, None, headers)
    html = urllib2.urlopen(req)
    html = html.read()
    page_soup = soup(html,"lxml")
    try:

        typecarburant = page_soup.find_all("h2", {"class": "font-normal fs12 no-margin ln22"})[2].text.replace('Type de carburant:','')
       # d = dat.split(":")[1]
        typecarburant =typecarburant.strip()
        return typecarburant


    except:
        return ""

def consult_marque(lien):
    global headers

    req = urllib2.Request(lien, None, headers)
    html = urllib2.urlopen(req)
    html = html.read()
    page_soup = soup(html,"lxml")
    try:

        marque = page_soup.find_all("h2", {"class": "font-normal fs12 no-margin ln22"})[3].text.replace('Marque','')
       # d = dat.split(":")[1]
        marque = marque.strip()
        return marque


    except:
        return ""

def consult_serie(lien):
    global headers

    req = urllib2.Request(lien, None, headers)
    html = urllib2.urlopen(req)
    html = html.read()
    page_soup = soup(html,"lxml")
    try:

        serie = page_soup.find_all("h2", {"class": "font-normal fs12 no-margin ln22"})[4].text
       # d = dat.split(":")[1]
        serie =serie.split(":")[1]
        return serie


    except:
        return ""
def consult_quartier(lien):
    global headers

    req = urllib2.Request(lien, None, headers)
    html = urllib2.urlopen(req)
    html = html.read()
    page_soup = soup(html,"lxml")
    try:

        secteur = page_soup.find_all("h2", {"class": "font-normal fs12 no-margin ln22"})[5].text.replace('Secteur:','')
       # d = dat.split(":")[1]
        secteur =secteur.strip()
        return secteur


    except:
        return ""

def consult_image(lien):
    global headers

    req = urllib2.Request(lien, None, headers)
    html = urllib2.urlopen(req)
    html = html.read()
    page_soup = soup(html,"lxml")
    try:

        image = page_soup.find('div',{'class','item active'}).img['src']       # d = dat.split(":")[1]
        return image


    except:
        return ""




def consult_type(lien):
    global headers

    req = urllib2.Request(lien, None, headers)
    html = urllib2.urlopen(req)
    html = html.read()
    page_soup = soup(html,"lxml")
    try:

        type = page_soup.find_all("h2", {"class": "font-normal fs12 no-margin ln22"})[6].text.replace('Type:','')
       # d = dat.split(":")[1]
        type =type.strip()
        return type


    except:
        return ""


for i in range(1 ,2):

    link = link0 + str(i)
    req = urllib2.Request(link, None, headers)
    html = urllib2.urlopen(req).read()
    page_soup = soup(html,"lxml")
    for j in range((i-1)*35+1,35*i+1):
        _id = "li-item-"+str(j)+" "
        divs = page_soup.findAll(id=_id)
        for div in divs :
            toDict = {}
            try :
                titre = div.find('h2').text
                #image = div.find('a')[0]
                description = div.find('span',{'class':'item-info-extra fs14'}).text.strip()
                description = ','.join([txt.strip() for txt in description.split('-')])
                typepropriete = description.split(",")[0]
                ville = description.split(",")[0]
                prix = div.find('div',{'class':'item-price'}).text.strip().split('DH')[0].strip()
                lien = div.find('a').get('href')
                date = div.find('div', {'class': 'item-age'}).text.strip()

                toDict['date'] = date
                toDict['ville'] = ville
                toDict['price'] = prix
                toDict['modele'] = consult_modele(lien)
                toDict['kilometrage'] = consult_kilo(lien)
                toDict['typecarburant']=consult_typecarburant(lien)
                toDict['marque'] = consult_marque(lien)
                toDict['serie']=consult_serie(lien)
                toDict['quartier']=consult_quartier(lien)
                toDict['type']=consult_type(lien)
                toDict['titre'] = titre
                toDict['descriptif'] = consult_paragraphe(lien)
                toDict['image'] = consult_image(lien)








                lien = div.find('a').get('href')

                #jsonarray = json.dumps(toDict)
                #with open("auto_avito.json", "a") as f:
                    #json.dump(toDict, f)
                collection.insert(toDict)






                print toDict
            except:
                pass
























            #print jsonarray
            #with open("auto_avito.json","a") as f:
                   # json.dump(toDict,f)
                   # collection.insert(toDict)
                   # print toDict
            #L.append(toDict.copy())

            #toDict.append(json.loads(line))
            #db.insert(toDict)









#df = pd.DataFrame.from_records(L)
#print df
#writer = pd.ExcelWriter('auto.xlsx')
#df.to_excel(writer, 'donnees')
#writer.save()
#print(L)
#df = pd.DataFrame.from_records(L)
#print "ok"
#print df
#writer = pd.ExcelWriter('output.xlsx')
#df.to_excel(writer, 'donnees')
#writer.save()


