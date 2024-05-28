# capa_acceso_datos.py
from pymongo import MongoClient

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class ConexionMongoDB:
    def __init__(self, uri):
        self.uri = uri
        self.client = None
        self.db = None

    def conectar(self, db_name):
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.db = self.client[db_name]

    def obtener_db(self):
        return self.db

uri = "mongodb+srv://MirandaYo:Paradoxa10@cluster0.zlkxkhi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
conexion = ConexionMongoDB(uri)
conexion.conectar('venta_boletos')
db = conexion.obtener_db()
