import pytest
import unittest
from pymongo import MongoClient
from capa_logica import LogicaBoletos
from capa_acceso_datos import ConexionMongoDB

from pymongo.server_api import ServerApi

# Configuración de la base de datos de prueba
uri = "mongodb+srv://MirandaYo:Paradoxa10@cluster0.zlkxkhi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["venta_boletos_test"]

# Instancia de la lógica de boletos usando la base de datos de prueba
logica_boletos = LogicaBoletos(db)

# Fixture para limpiar la base de datos después de cada prueba
@pytest.fixture(autouse=True)
def limpiar_db():
    db["boletos_1"].delete_many({})
    db["pelicula"].delete_many({})
    db["sala_cine_1"].delete_many({})
    yield
    db["boletos_1"].delete_many({})
    db["pelicula"].delete_many({})
    db["sala_cine_1"].delete_many({})

def test_crear_boleto():
    # Agregar película y sala de cine de prueba
    pelicula_id = logica_boletos.crear_pelicula("Test Movie", 120, "Test Genre")
    sala_cine = {
        "Nombre": "Test Sala",
        "Cantidad Asientos": "50"
    }
    sala_id = db["sala_cine_1"].insert_one(sala_cine).inserted_id

    # Crear boleto
    orden_compra = "OC12345"
    cantidad = 10
    nombre_pelicula = "Test Movie"
    nombre_sala = "Test Sala"
    boleto_id = logica_boletos.crear_boleto(orden_compra, cantidad, nombre_pelicula, nombre_sala)

    # Verificar que el boleto se haya creado correctamente
    assert boleto_id is not None
    boleto = db["boletos_1"].find_one({"_id": boleto_id})
    assert boleto["orden_compra"] == orden_compra
    assert boleto["Cantidad"] == cantidad
    assert boleto["pelicula"] == pelicula_id
    assert boleto["sala_cine"] == sala_id

def test_no_crear_boleto_sala_inexistente():
    # Agregar película de prueba
    logica_boletos.crear_pelicula("Test Movie", 120, "Test Genre")

    # Intentar crear boleto con sala inexistente
    orden_compra = "OC12345"
    cantidad = 10
    nombre_pelicula = "Test Movie"
    nombre_sala = "Sala Inexistente"
    boleto_id = logica_boletos.crear_boleto(orden_compra, cantidad, nombre_pelicula, nombre_sala)

    # Verificar que no se haya creado el boleto
    assert boleto_id is None

def test_no_crear_boleto_cantidad_excesiva():
    # Agregar película y sala de cine de prueba
    logica_boletos.crear_pelicula("Test Movie", 120, "Test Genre")
    sala_cine = {
        "Nombre": "Test Sala",
        "Cantidad Asientos": "10"
    }
    db["sala_cine_1"].insert_one(sala_cine)

    # Intentar crear boleto con cantidad excesiva
    orden_compra = "OC12345"
    cantidad = 20
    nombre_pelicula = "Test Movie"
    nombre_sala = "Test Sala"
    boleto_id = logica_boletos.crear_boleto(orden_compra, cantidad, nombre_pelicula, nombre_sala)

    # Verificar que no se haya creado el boleto
    assert boleto_id is None


def test_obtener_boletos():
    # Agregar películas y salas de cine de prueba a la base de datos
    pelicula_1_id = db["pelicula"].insert_one({"Nombre": "Pelicula 1"}).inserted_id
    pelicula_2_id = db["pelicula"].insert_one({"Nombre": "Pelicula 2"}).inserted_id
    sala_1_id = db["sala_cine_1"].insert_one({"Nombre": "Sala 1", "Cantidad Asientos": 100}).inserted_id
    sala_2_id = db["sala_cine_1"].insert_one({"Nombre": "Sala 2", "Cantidad Asientos": 150}).inserted_id

    # Agregar boletos de prueba a la base de datos
    boleto_1 = {
        "orden_compra": "OC1",
        "Cantidad": 5,
        "pelicula": pelicula_1_id,
        "sala_cine": sala_1_id
    }
    boleto_2 = {
        "orden_compra": "OC2",
        "Cantidad": 10,
        "pelicula": pelicula_2_id,
        "sala_cine": sala_2_id
    }
    db["boletos_1"].insert_one(boleto_1)
    db["boletos_1"].insert_one(boleto_2)

    # Obtener boletos y verificar
    boletos = logica_boletos.obtener_boletos()
    assert len(boletos) == 2

def test_actualizar_boleto():
    # Agregar película y sala de cine de prueba a la base de datos
    pelicula_id = db["pelicula"].insert_one({"Nombre": "Pelicula 1"}).inserted_id
    sala_id = db["sala_cine_1"].insert_one({"Nombre": "Sala 1", "Cantidad Asientos": 100}).inserted_id

    # Agregar boleto de prueba a la base de datos
    boleto = {
        "orden_compra": "OC1",
        "Cantidad": 5,
        "pelicula": pelicula_id,
        "sala_cine": sala_id
    }
    boleto_id = db["boletos_1"].insert_one(boleto).inserted_id

    # Actualizar boleto y verificar
    nueva_cantidad = 10
    actualizacion = {"Cantidad": nueva_cantidad}
    logica_boletos.actualizar_boleto(str(boleto_id), actualizacion)
    boleto_actualizado = db["boletos_1"].find_one({"_id": boleto_id})
    assert boleto_actualizado["Cantidad"] == nueva_cantidad



##PRUEBA INTEGRACIÓN
class TestLogicaBoletos(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Replace with your actual MongoDB connection URI
        uri = "mongodb+srv://MirandaYo:Paradoxa10@cluster0.zlkxkhi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

        # Create a new client and connect to the server
        cls.client = MongoClient(uri)
        cls.db = cls.client.venta_boletos
        cls.logica_boletos = LogicaBoletos(cls.db)

    @classmethod
    def tearDownClass(cls):
        cls.client.close()

    def test_conexion_exitosa(self):
        # Verificar si la conexión a la base de datos se establece correctamente
        self.assertIsNotNone(self.client)

    def test_insertar_documento(self):
        # Insertar un documento de prueba en la base de datos
        documento_prueba = {"campo": "valor"}
        resultado = self.db.prueba.insert_one(documento_prueba)

        # Verificar que la inserción fue exitosa
        self.assertIsNotNone(resultado.inserted_id)

if __name__ == "__main__":
    unittest.main()