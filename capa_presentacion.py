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

def main():
    uri = "mongodb+srv://MirandaYo:Paradoxa10@cluster0.zlkxkhi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    conexion = ConexionMongoDB(uri)
    conexion.conectar("venta_boletos")
    logica_boletos = LogicaBoletos(conexion.obtener_db())

    while True:
        menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            orden_compra = input("Número de Orden de Compra: ")
            cantidad = int(input("Cantidad: "))
            nombre_pelicula = input("Nombre de la Película: ")
            nombre_sala = input("Nombre de la Sala de Cine: ")
            boleto_id = logica_boletos.crear_boleto(orden_compra, cantidad, nombre_pelicula, nombre_sala)
            if boleto_id:
                print(f"Reserva de boleto creada con ID: {boleto_id}")

        elif opcion == '2':
            boletos = logica_boletos.obtener_boletos()
            for boleto in boletos:
                print(boleto)

        elif opcion == '3':
            boleto_id = input("ID de la Reserva a actualizar: ")
            orden_compra = input("Nuevo Número de Orden de Compra (dejar en blanco para no cambiar): ")
            cantidad = input("Nueva Cantidad (dejar en blanco para no cambiar): ")
            nombre_pelicula = input("Nuevo Nombre de Película (dejar en blanco para no cambiar): ")
            nombre_sala = input("Nuevo Nombre de la Sala de Cine (dejar en blanco para no cambiar): ")

            actualizacion = {}
            if orden_compra:
                actualizacion["orden_compra"] = orden_compra
            if cantidad:
                actualizacion["Cantidad"] = int(cantidad)
            if nombre_pelicula:
                actualizacion["Nombre_pelicula"] = nombre_pelicula
            if nombre_sala:
                actualizacion["Nombre_sala"] = nombre_sala

            result = logica_boletos.actualizar_boleto(boleto_id, actualizacion)
            if result and result.modified_count > 0:
                print("Reserva de boleto actualizada correctamente")
            else:
                print("No se encontró la reserva o no hubo cambios")

        elif opcion == '4':
            boleto_id = input("ID de la Reserva a eliminar: ")
            result = logica_boletos.eliminar_boleto(boleto_id)
            if result.deleted_count > 0:
                print("Reserva de boleto eliminada correctamente")
            else:
                print("No se encontró la reserva")

        elif opcion == '5':
            nombre = input("Nombre de la Película: ")
            duracion_minutos = int(input("Duración (minutos): "))
            genero = input("Género: ")
            pelicula_id = logica_boletos.crear_pelicula(nombre, duracion_minutos, genero)
            print(f"Película creada con ID: {pelicula_id}")

        elif opcion == '6':
            peliculas = logica_boletos.obtener_peliculas()
            for pelicula in peliculas:
                print(pelicula)

        elif opcion == '7':
            pelicula_id = input("ID de la Película a actualizar: ")
            nombre = input("Nuevo Nombre (dejar en blanco para no cambiar): ")
            duracion_minutos = input("Nueva Duración (dejar en blanco para no cambiar): ")
            genero = input("Nuevo Género (dejar en blanco para no cambiar): ")

            actualizacion = {}
            if nombre:
                actualizacion["Nombre"] = nombre
            if duracion_minutos:
                actualizacion["duracion_minutos"] = int(duracion_minutos)
            if genero:
                actualizacion["genero"] = genero

            result = logica_boletos.actualizar_pelicula(pelicula_id, actualizacion)
            if result.modified_count > 0:
                print("Película actualizada correctamente")
            else:
                print("No se encontró la película o no hubo cambios")

        elif opcion == '8':
            pelicula_id = input("ID de la Película a eliminar: ")
            result = logica_boletos.eliminar_pelicula(pelicula_id)
            if result.deleted_count > 0:
                print("Película eliminada correctamente")
            else:
                print("No se encontró la película")

        elif opcion == '9':
            print("Saliendo del sistema")
            break

        else:
            print("Opción no válida, intente de nuevo")

if __name__ == "__main__":
    main()

##45