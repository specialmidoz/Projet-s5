from pymongo import  MongoClient
client = MongoClient()
db = client['ps5']
collection  = db['voiture']



