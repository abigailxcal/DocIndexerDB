from pymongo import MongoClient
import datetime


def connectDataBase():
    DB_NAME = "CPP"
    DB_HOST = "localhost"
    DB_PORT = 27017

    try:

        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]

        return db

    except:
        print("Database not connected successfully")



def createDocument(col, docId, docText, docTitle, docDate, docCat):
    terms = [term.strip("!@#$%^&*()_+[]{};:'\"<>,.?/~`") for term in docText.lower().split(" ")]
    
    # create a dictionary to count how many times each term appears in the document.
    term_count = dict([(term,terms.count(term)) for term in terms ])
    
    # create a list of dictionaries to include term objects. [{"term", count, num_char}]
    term_obj_dict = [{term: [count, len(term)]} for term, count in term_count.items()]
    num_chars = 0
    for term,count in term_count.items():
            num_chars += len(term)*count
    date = datetime.datetime.strptime(docDate, "%Y/%m/%d")

    #Producing a final document as a dictionary including all the required document fields
    document = {"_id": docId,
                "text":docText,
                "title": docTitle,
                "num_chars": num_chars,
                "date": date.date(),
                "category": docCat,
                "terms": [
                    {"term": term, "term_count": data[0], "num_chars": data[1]}
                    for term_data in term_obj_dict
                    for term, data in term_data.items()
                ]
                }
    
    # Insert the document
    col.insert_one(document)


def deleteDocument(col, docId):
    # Delete the document from the database
    col.delete_one({"_id":docId})


def updateDocument(col, docId, docText, docTitle, docDate, docCat):
    # Delete the document
    deleteDocument(col,docId)

    # Create the document with the same id
    createDocument(col, docId, docText, docTitle, docDate, docCat)
    


def getIndex(col):

    # Query the database to return the documents where each term occurs with their corresponding count. 
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    pipeline= [ 
        {'$unwind': {'path': '$terms'}}, 
        {'$project': {'term': '$terms.term',
                    'title': '$title',
                    'term_count': '$terms.term_count'} },
        {'$group': {'_id': '$term',
                    'documents': {
                        '$push': {
                             'title':'$title',
                             'term_count':'$term_count'}}
                    }},
        {'$sort':{'_id':1}}]
    
    index = col.aggregate(pipeline)
    inverted_index =''

    for term in index:
        inverted_index+="'"+term['_id']+"': "
        for i in range(len(term['documents'])):
            inverted_index+=term['documents'][i]['title']+":"+str(term['documents'][i]['term_count'])
            if i != len(term['documents'])-1:
                inverted_index+=", "
        inverted_index+="\n"

    return inverted_index

