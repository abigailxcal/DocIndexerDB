from pymongo import MongoClient
import datetime

def connectDataBase():

    # Creating a database connection object using pymongo

    DB_NAME = "CPP"
    DB_HOST = "localhost"
    DB_PORT = 27017

    try:

        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]

        return db

    except:
        print("Database not connected successfully")

def createUser(col, id, name, email):

    # Value to be inserted
    user = {"_id": id,
            "name": name,
            "email": email,
            }

    # Insert the document
    col.insert_one(user)

def updateUser(col, id, name, email):

    # User fields to be updated
    user = {"$set": {"name": name, "email": email} }

    # Updating the user
    col.update_one({"_id": id}, user)

def deleteUser(col, id):

    # Delete the document from the database
    col.delete_one({"_id": id})

def getUser(col, nameUser):

    user = col.find_one({"name":nameUser})

    if user:
        return str(user['_id']) + " | " + user['name'] + " | " + user['email']
    else:
        return []

def createComment(col, id, id_user, text, dateTime):

    # Comments to be included
    comments = {"$push": {"comments": {"id": id,
                                       "message": text,
                                       "datetime": datetime.datetime.strptime(dateTime, "%m/%d/%Y %H:%M:%S")} }}

    # Updating the user document
    col.update_one({"_id": id_user}, comments)

def updateComment(col, id_user, id, text, dateTime):

    # User fields to be updated
    comment = {"$set": {"comments.$.message": text} }

    # Updating the user
    col.update_one({"_id": id_user, "comments.id": id}, comment)

def deleteComment(col, id_user, id):

    # Comments to be delete
    comments = {"$pull": {"comments": {"id": id} }}

    # Updating the user document
    col.update_one({"_id": id_user}, comments)

def getChat(col):

    # creating a document for each message
    pipeline = [
                 {"$unwind": { "path": "$comments" }},
                 {"$sort": {"comments.datetime": 1}}
               ]

    messages = col.aggregate(pipeline)

    chat = ""

    for msn in messages:
        chat += msn['name'] + " | " + msn['comments']['message'] + " | " + str(msn['comments']['datetime']) + "\n"

    return chat