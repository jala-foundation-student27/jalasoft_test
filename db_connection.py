from pymongo import MongoClient

client = MongoClient(host="localhost",port=27017)
db = client.jalasoft_test_db

def get_todo_collection():  # return the collection on the jalasoft_test_db
    collection = db.todo_list_collection
    return collection

def get_db():
    return db