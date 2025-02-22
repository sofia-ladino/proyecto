from pymongo import MongoClient
import certifi, gridfs

MONGO_URI = 'mongodb+srv://sofialadinodocumentos:LXUpvjMTib69WCOj@cluster0.z27wp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client["db_proyecto"]
    except ConnectionError:
        print ('error de conexión con la bd')
    return db

# Obtener la conexión antes de usarla
db = dbConnection()

# Solo crear GridFS si la conexión fue exitosa

fs = gridfs.GridFS(db)