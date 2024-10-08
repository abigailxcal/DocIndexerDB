import psycopg2
import string

def connectDataBase():
    try:
        conn = psycopg2.connect(
            dbname="",
            user="postgres",
            password="",
            host="localhost",
            port="5432"
        )
        return conn
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)

def createCategory(cur, catId, catName):
    try:
        cur.execute("INSERT INTO Categories(category_id, name) VALUES (%s, %s)", (catId, catName))
        cur.connection.commit()
    except psycopg2.Error as e:
        print("Error creating category:", e)

def createDocument(cur, docId, docText, docTitle, docDate, docCat):

    try:
        # 1 Get the category id based on the informed category name
        cur.execute("SELECT category_id FROM Categories WHERE name = %s", (docCat,))
        catId = cur.fetchone()[0]

        # 2 Insert the document in the database. For num_chars, discard the spaces and punctuation marks.
        custom_punctuation = "!@#$%^&*()_+[]{};:'\"<>,.?/~`"  # Customize this list as needed
        num_chars = len(docText) - docText.count(' ') - sum(docText.count(p) for p in custom_punctuation)

        cur.execute("INSERT INTO Documents(doc_number, text, title, num_chars, date, category_id) VALUES (%s, %s, %s, %s, %s, %s)", (docId, docText, docTitle, num_chars, docDate, catId))

        # 3 Update the potential new terms.
        terms = set([term.strip(string.punctuation).lower() for term in docText.split()])

        for term in terms:
            cur.execute("INSERT INTO Terms(term, num_chars) VALUES (%s, %s) ON CONFLICT DO NOTHING",(term, len(term)))

        # 4 Update the index
        for term in terms:
            count = docText.lower().count(term)
            cur.execute("INSERT INTO Document_term_relationship(doc_number, term, count) VALUES (%s, %s, %s)", (docId, term, count))

        cur.connection.commit()

    except psycopg2.Error as e:
        print("Error creating document:", e)

def deleteDocument(cur, docId):
    try:
        # 1 Query the index based on the document to identify terms
        cur.execute("SELECT term FROM INTO Document_term_relationship WHERE doc_number = %s", (docId,))
        terms = [row[0] for row in cur.fetchall()]

        for term in terms:
            cur.execute("DELETE FROM INTO Document_term_relationship WHERE doc_number = %s AND term = %s", (docId, term))
            # Check if there are no more occurrences of the term in another document
            cur.execute("SELECT COUNT(*) FROM INTO Document_term_relationship WHERE term = %s", (term,))
            count = cur.fetchone()[0]
            if count == 0:
                cur.execute("DELETE FROM Terms WHERE term = %s", (term,))

        # 2 Delete the document from the database
        cur.execute("DELETE FROM Documents WHERE doc_number = %s", (docId,))
        cur.connection.commit()

    except psycopg2.Error as e:
        print("Error deleting document:", e)

def updateDocument(cur, docId, docText, docTitle, docDate, docCat):
    try:
        # 1 Delete the document
        deleteDocument(cur, docId)

        # 2 Create the document with the same id
        createDocument(cur, docId, docText, docTitle, docDate, docCat)

    except psycopg2.Error as e:
        print("Error updating document:", e)

def getIndex(cur):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    try:
        cur.execute("SELECT term, ARRAY_AGG(DISTINCT title || ':' || count) FROM INTO Document_term_relationship " +
                    "JOIN Documents ON INTO Document_term_relationship.doc_number = Documents.doc_number " +
                    "GROUP BY term")
        index = {row[0]: ', '.join(row[1]) for row in cur.fetchall()}
        return index
    except psycopg2.Error as e:
        print("Error getting index:", e)

def closeDataBase(conn):
    conn.close()