# capa_acceso_datos.py
from pymongo import MongoClient

class CineDatos:
    def __init__(self):
        self.cliente = MongoClient('mongodb://localhost:27017/')
        self.db = self.cliente['cine_db']
        self.boletas = self.db['boletas']

    def obtener_boletas(self):
        return list(self.boletas.find())

    def obtener_boleta_por_asiento(self, asiento):
        return self.boletas.find_one({'asiento': asiento})

    def actualizar_boleta(self, asiento, datos_actualizados):
        resultado = self.boletas.update_one({'asiento': asiento}, {'$set': datos_actualizados})
        return resultado.modified_count > 0
