import json
from pymongo import MongoClient
import pymongo
with open('C:/Users/MyPC/Documents/Nam4/Blockchain/TrainingStudents/3.Backend/TrainingAPI/app/databases/collections.json', 'r') as f:
    collections = json.load(f)
client = MongoClient('mongodb://localhost:27017/')
db = client['trainingSanic']
for collection_name, collection_data in collections.items():
    db.create_collection(collection_data['collection_name'])
for collection_name, collection_data in collections.items():
    collection = db[collection_data['collection_name']]
    for field_name, field_type in collection_data['document_fields'].items():
        collection.create_index([(field_name, pymongo.ASCENDING)])
