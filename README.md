# Sistema de Gestión de Boletos del Cine


**IDEA GENERAL:** El objetivo de este proyecto es desarrollar un software sencillo para la compra y gestión de boletos de cine, implementando operaciones CRUD (Crear, Leer, Actualizar, Eliminar). El software está diseñado con una arquitectura de tres capas y utiliza MongoDB para el almacenamiento de datos.

**Arquitectura del Sistema:** El sistema está dividido en tres capas principales:

**Capa de presentación :** 
- Esta capa gestiona la interacción entre el usuario y la aplicación.
- La interfaz de usuario se maneja a través de la terminal, donde los usuarios pueden seleccionar opciones del menú para realizar diferentes operaciones.

**Capa de Lógica :** 
- En esta capa se define toda la lógica de negocio de la aplicación.
- Aquí se encuentran los métodos que permiten gestionar las reservas de boletos y la información de las películas y salas de cine.

**Capa de Acceso a Datos :** 
- Esta capa maneja todas las interacciones con la base de datos MongoDB.
- Defina los métodos para conectar, insertar, actualizar y eliminar datos en la base de datos.

