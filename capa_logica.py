# capa_logica.py
from bson.objectid import ObjectId
from capa_acceso_datos import ConexionMongoDB

class LogicaBoletos:
    def __init__(self, db):
        self.db = db
        self.boletos_collection = self.db['boletos_1']
        self.salas_collection = self.db['sala_cine_1']
        self.sucursales_collection = self.db['sucursal']
        self.peliculas_collection = self.db['pelicula']

    def crear_boleto(self, orden_compra, cantidad, nombre_pelicula, nombre_sala):
        pelicula = self.peliculas_collection.find_one({"Nombre": nombre_pelicula})
        if not pelicula:
            print(f"Error: La película '{nombre_pelicula}' no existe en la base de datos.")
            return None

        sala = self.salas_collection.find_one({"Nombre": nombre_sala})
        if not sala:
            print(f"Error: La sala '{nombre_sala}' no existe en la base de datos.")
            return None

        cantidad_asientos = int(sala["Cantidad Asientos"])
        boletos_reservados = self.boletos_collection.aggregate([
            {"$match": {"sala_cine": sala["_id"]}},
            {"$group": {"_id": None, "total_reservados": {"$sum": "$Cantidad"}}}
        ])
        total_reservados = 0
        for reservados in boletos_reservados:
            total_reservados = reservados["total_reservados"]

        if total_reservados + cantidad > cantidad_asientos:
            print(f"Error: No hay suficientes asientos disponibles en la sala '{nombre_sala}'.")
            return None

        boleto = {
            "orden_compra": orden_compra,
            "Cantidad": cantidad,
            "pelicula": pelicula["_id"],
            "sala_cine": sala["_id"]
        }
        result = self.boletos_collection.insert_one(boleto)
        return result.inserted_id

    def obtener_boletos(self):
        boletos = list(self.boletos_collection.find())
        for boleto in boletos:
            pelicula = self.peliculas_collection.find_one({"_id": boleto["pelicula"]})
            sala = self.salas_collection.find_one({"_id": boleto["sala_cine"]})
            boleto["Nombre_pelicula"] = pelicula["Nombre"] if pelicula else "Desconocido"
            boleto["Nombre_sala"] = sala["Nombre"] if sala else "Desconocido"
        return boletos

    def obtener_boleto_por_id(self, boleto_id):
        boleto = self.boletos_collection.find_one({"_id": ObjectId(boleto_id)})
        if boleto:
            pelicula = self.peliculas_collection.find_one({"_id": boleto["pelicula"]})
            sala = self.salas_collection.find_one({"_id": boleto["sala_cine"]})
            boleto["Nombre_pelicula"] = pelicula["Nombre"] if pelicula else "Desconocido"
            boleto["Nombre_sala"] = sala["Nombre"] if sala else "Desconocido"
        return boleto

    def actualizar_boleto(self, boleto_id, actualizacion):
        if "Nombre_pelicula" in actualizacion:
            pelicula = self.peliculas_collection.find_one({"Nombre": actualizacion["Nombre_pelicula"]})
            if not pelicula:
                print(f"Error: La película '{actualizacion['Nombre_pelicula']}' no existe en la base de datos.")
                return None
            actualizacion["pelicula"] = pelicula["_id"]
            del actualizacion["Nombre_pelicula"]

        if "Nombre_sala" in actualizacion:
            sala = self.salas_collection.find_one({"Nombre": actualizacion["Nombre_sala"]})
            if not sala:
                print(f"Error: La sala '{actualizacion['Nombre_sala']}' no existe en la base de datos.")
                return None
            actualizacion["sala_cine"] = sala["_id"]
            del actualizacion["Nombre_sala"]

        return self.boletos_collection.update_one({"_id": ObjectId(boleto_id)}, {"$set": actualizacion})

    def eliminar_boleto(self, boleto_id):
        return self.boletos_collection.delete_one({"_id": ObjectId(boleto_id)})

    # Operaciones CRUD para Películas
    def crear_pelicula(self, nombre, duracion_minutos, genero):
        pelicula = {
            "Nombre": nombre,
            "duracion_minutos": duracion_minutos,
            "genero": genero
        }
        result = self.peliculas_collection.insert_one(pelicula)
        return result.inserted_id

    def obtener_peliculas(self):
        return list(self.peliculas_collection.find())

    def obtener_pelicula_por_id(self, pelicula_id):
        return self.peliculas_collection.find_one({"_id": ObjectId(pelicula_id)})

    def actualizar_pelicula(self, pelicula_id, actualizacion):
        return self.peliculas_collection.update_one({"_id": ObjectId(pelicula_id)}, {"$set": actualizacion})

    def eliminar_pelicula(self, pelicula_id):
        return self.peliculas_collection.delete_one({"_id": ObjectId(pelicula_id)})

##69