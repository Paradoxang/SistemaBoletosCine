Python 3.10.4 (tags/v3.10.4:9d38120, Mar 23 2022, 23:13:41) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
# capa_presentacion.py
from capa_logica import CineLogica

class CinePresentacion:
    def __init__(self):
        self.logica = CineLogica()

    def mostrar_menu(self):
        while True:
            print("\n=== Sistema de Reserva de Boletas de Cine ===")
            print("1. Ver boletas")
            print("2. Reservar boleta")
            print("3. Cancelar reserva")
            print("4. Salir")
            opcion = input("Seleccione una opción: ")
            if opcion == '1':
                self.ver_boletas()
            elif opcion == '2':
                self.reservar_boleta()
            elif opcion == '3':
                self.cancelar_reserva()
            elif opcion == '4':
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def ver_boletas(self):
        boletas = self.logica.obtener_boletas()
        for boleta in boletas:
            print(f"ID: {boleta['_id']}, Película: {boleta['pelicula']}, Asiento: {boleta['asiento']}, Reservado: {boleta['reservado']}")

    def reservar_boleta(self):
        pelicula = input("Ingrese el nombre de la película: ")
        asiento = input("Ingrese el número de asiento: ")
        resultado = self.logica.reservar_boleta(pelicula, asiento)
        if resultado:
            print("Boleta reservada con éxito.")
        else:
            print("Error al reservar la boleta.")

    def cancelar_reserva(self):
        asiento = input("Ingrese el número de asiento a cancelar: ")
        resultado = self.logica.cancelar_reserva(asiento)
        if resultado:
            print("Reserva cancelada con éxito.")
        else:
            print("Error al cancelar la reserva.")

if __name__ == "__main__":
    app = CinePresentacion()
    app.mostrar_menu()
