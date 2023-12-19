from dotenv import load_dotenv , find_dotenv
import os 
import pprint
from pymongo import MongoClient 
load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PWD")


connection_string = f"mongodb+srv://Lida:{password}@cluster0.ejidejg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

client = MongoClient(connection_string)

dbs = client.list_database_names()
print(dbs)
test_db = client.test
collections = test_db.list_collection_names()
print(collections)

def insert_test_doc():
    collection = test_db.test
    test_document = {
        "name" : "Tim" ,
        "type" : "Test"
    }
    inserted_id =  collection.insert_one(test_document).inserted_id
    print(inserted_id)

production = client.production
person_collection = production.person_collection
def create_documents():
    first_names = ["Tim" ,"Sarah" , "Jennifer" , "Jose" , "Bard" , "Allen"]
    last_names = ["Rusica" , "Smith" , "Bart" , "Cater" , "Pit" , "Geral",]
    ages = [21,40,23,19,34,67]
    
    docs = []
    for first_name , last_name , age in zip(first_names,last_names,ages):
        doc = {"first_name":first_name ,"last_name": last_name,"age" :age}
        docs.append(doc)
        # person_collection.insert_one(doc)
    person_collection.insert_many(docs)


printer = pprint.PrettyPrinter()

def find_all_people():
    people = person_collection.find()

    for person in people: 
        printer.pprint(person)        


def find_tim():
    tim = person_collection.find_one({"first_name": "Tim"})
    printer.pprint(tim)

def count_all_people():
    count = person_collection.count_documents(filter={})
    print("Number of people" , count)

def get_person_by_id(person_id):
    from bson.objectid import ObjectId

    _id = ObjectId(person_id)
    person = person_collection.find_one({"_id":_id})
    printer.pprint(person)

#get_person_by_id("6581f00cb0f8367f2871f49f")
    
def get_age_range(min_age,max_age):
    query = {"$and":[
            {"age": { "$gte": min_age }},
            {"age": { "$lte": max_age }},
        ]}
    people = person_collection.find(query).sort("age")
    for person in people:
        printer.pprint(person)

#get_age_range(20, 35)
        
def project_columns():
    columns = {"_id":0, "first_name":1, "last_name":1}
    people = person_collection.find({}, columns)
    for person in people:
        printer.pprint(person)

#project_columns()    
        
def update_person_by_id(person_id):
    from bson.objectid import ObjectId

    _id = ObjectId(person_id)

   # all_updates = {
   #     "$set": {"new_field":True},
   #     "$inc":{"age":1},
   #     "$rename":{"first_time":"first","last_name":"last"}
   # }
   # person_collection.update_one({"_id":_id},all_updates)
    
   # person_collection.update_one({"_id":_id},{"$unset":{"new_field":""}})

def replace_one(person_id):
    from bson.objectid import ObjectId
    _id = ObjectId(person_id)

    new_doc = {
        "first_name": "new first name",
        "last_name": "new last name",
        "age":  100
    }

    person_collection.replace_one({"_id": _id }, new_doc)

replace_one("6581f00cb0f8367f2871f49e")

#----------------------------------------------------------------


address = {
    "_id":"6581f00cb0f8367f2871f49e",
    "street":"Bay Street",
    "number":2706,
    "city":"San Francisco" ,
    "country":"United States",
    "zip" : "94107",
    "owner_id":"6581f00cb0f8367f2871f49f"
}

def add_address_embed(person_id,address):
    from bson.objectid import ObjectId
    _id = ObjectId(person_id)

    address = address.copy()
    address["owner_id"] = person_id

    address_collection = production.address
    address_collection.insert_one(address)

    person_collection.update_one({"_id":_id},{"$addToSet":{'addresses':address}})

add_address_embed('6581f00cb0f8367f2871f49f',address)