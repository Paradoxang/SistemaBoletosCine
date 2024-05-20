# capa_logica.py
from capa_acceso_datos import CineDatos

class CineLogica:
    def __init__(self):
        self.datos = CineDatos()

    def obtener_boletas(self):
        return self.datos.obtener_boletas()

    def reservar_boleta(self, pelicula, asiento):
        boleta = self.datos.obtener_boleta_por_asiento(asiento)
        if boleta and not boleta['reservado']:
            return self.datos.actualizar_boleta(asiento, {'reservado': True, 'pelicula': pelicula})
        return False

    def cancelar_reserva(self, asiento):
        boleta = self.datos.obtener_boleta_por_asiento(asiento)
        if boleta and boleta['reservado']:
            return self.datos.actualizar_boleta(asiento, {'reservado': False, 'pelicula': None})
        return False
