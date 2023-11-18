from pymongo import MongoClient

client = MongoClient(host="localhost",port=27017)

def get_todo_collection():  # return the collection containing the todo_list documents
    db = client.jalasoft_test_db
    collection = db.todo_list_collection
    return collection

def get_db(): # return the database for acessing other collections (softed deleted todo_list) 
    db = client.jalasoft_test_db
    return db