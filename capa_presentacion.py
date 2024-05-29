from capa_logica import LogicaBoletos
from capa_acceso_datos import ConexionMongoDB
def menu():
    print("Bienvenido al sistema de gestión de boletos del Cinema")
    print("1. Crear Reserva de Boleto")
    print("2. Ver Reservas de Boletos")
    print("3. Actualizar Reserva de Boleto")
    print("4. Eliminar Reserva de Boleto")
    print("5. Crear Película")
    print("6. Ver Películas")
    print("7. Actualizar Película")
    print("8. Eliminar Película")
    print("9. Salir")

def main(conexion):
    logica_boletos = LogicaBoletos(conexion.obtener_db())

    opciones = {
        '1': ('crear_boleto', ['Orden de Compra', 'Cantidad', 'Nombre de la Película', 'Nombre de la Sala de Cine']),
        '2': ('obtener_boletos', []),
        '3': ('actualizar_boleto', ['Orden de Compra a actualizar', 'Nueva Cantidad', 'Nuevo Nombre de Película', 'Nuevo Nombre de la Sala de Cine']),
        '4': ('eliminar_boleto', ['Orden de Compra a eliminar']),
        '5': ('crear_pelicula', ['Nombre de la Película', 'Duración (minutos)', 'Género']),
        '6': ('obtener_peliculas', []),
        '7': ('actualizar_pelicula', ['ID de la Película a actualizar', 'Nuevo Nombre', 'Nueva Duración', 'Nuevo Género']),
        '8': ('eliminar_pelicula', ['ID de la Película a eliminar']),
        '9': (None, [])
    }

    while True:
        menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '9':
            print("Saliendo del sistema")
            break

        accion, parametros = opciones.get(opcion, (None, None))
        if accion:
            if parametros:
                accion_params = []
                for param in parametros:
                    valor = input(f"{param}: ")
                    if param in {'Cantidad', 'Duración (minutos)'}:
                        valor = int(valor)
                    accion_params.append(valor)
                result = getattr(logica_boletos, accion)(*accion_params)
                if result:
                    print("Operación realizada con éxito")
                else:
                    print("Ocurrió un error durante la operación")
            else:
                for item in getattr(logica_boletos, accion)():
                    print(item)
        else:
            print("Opción no válida, intente de nuevo")

if __name__ == "__main__":
    uri = "mongodb+srv://MirandaYo:Paradoxa10@cluster0.zlkxkhi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    conexion = ConexionMongoDB(uri)
    conexion.conectar("venta_boletos")
    main(conexion)

##69