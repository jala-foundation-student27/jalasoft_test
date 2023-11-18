from flask import Blueprint,jsonify,request,abort
from todo_list_model import Todo_list_model,Status
from db_connection import get_todo_collection,get_db
from bson import ObjectId
import datetime

todo_bp = Blueprint("todo_bp",__name__)

db=get_db()
soft_deleted_todo_list = db.soft_deleted_todo_list
todo_collection = get_todo_collection()

@todo_bp.route('/todo_list/<id>',methods=["GET"])
def get(id):
    try:
        response = todo_collection.find_one({"_id":ObjectId(id)}) # 404 If object is not found
        response.update({"_id":id})
    except:
        abort(404)
    return jsonify(response)


@todo_bp.route('/todo_list/<id>',methods=["PUT"])
def put(id):
    try:
        request_json = request.get_json() # 400 if request cant be parsed to json (invalid request)
        now = datetime.datetime.now()
        parsed_data = {"task":request_json["task"],  
                    "deadline":request_json["deadline"],
                        "category":request_json["category"],
                        "status":Status(request_json["status"]),
                        "description":request_json["description"],
                        "lastUpdated":now}
        Todo_list_model(**parsed_data)      # validate if the request match the todo_list model
        insert_response = todo_collection.replace_one({"_id":ObjectId(id)},request_json) 
    except:                                                                                             
        abort(400)
    request_json.update({"_id":id,"lastUpdated":now}) # Object id cant be casted to json, need to parse to return the 
    return jsonify(request_json),201


@todo_bp.route('/todo_list',methods=["POST"])
def post():
    try:
        request_json = request.get_json() # 400 if request cant be parsed to json (invalid request)
        now = datetime.datetime.now()
        parsed_data = {"task":request_json["task"],
                    "deadline":request_json["deadline"],
                        "category":request_json["category"],
                        "status":Status(request_json["status"]),
                        "description":request_json["description"],
                        "lastUpdated":now
                        }
        #Todo_list_model(**parsed_data)  # validate if the request match the todo_list model
        insert_response = todo_collection.insert_one(request_json) # Object id cant be casted to json
    except:
        abort(400)
    request_json.update({"_id":str(request_json["_id"]),"lastUpdated":now}) # conversion of types for returning json
    return jsonify(request_json),201,{"location":f"/todo_list/{insert_response.inserted_id}"} # header will contain the created  ObjectID


@todo_bp.route('/todo_list/<id>',methods=["DELETE"]) # deleted files will go to soft deleted documents and removed from todo_colection
def delete(id): 
    try:
        response = todo_collection.find_one({"_id":ObjectId(id)})
    except:
        abort(404)
    try:
        soft_deleted_todo_list.insert_one(response)
        todo_collection.delete_one({"_id":ObjectId(id)})
    except:
        abort(400)
    return "",204

@todo_bp.route('/todo_list/deleted/<id>',methods=["GET"]) # Search for de document on the Soft_deleted colection
def get_soft_deleted(id):
    try:
        response = soft_deleted_todo_list.find_one({"_id":ObjectId(id)}) # 404 if object not found on softed_deleted colection
        response.update({"_id":id})
    except:
        abort(404)
    return jsonify(response)


# ERROR HANDLING
@todo_bp.errorhandler(400) 
def invalid_request(e):
    return jsonify({"error":"invalid request"}),400

@todo_bp.errorhandler(404)
def invalid_request(e):
    return jsonify({"error":"Object Not Found"}),404