import os
from src.conexion import conectarBD
from src.controladores.clientes import (
    buscarClienteSuscripcion, 
    actualizarCliente, 
    crearSuscripcion, 
    cancelarSuscripcion
)
from src.controladores.inventario import (
    obtenerProductos,
    crearProducto,
    buscarProductoPorId,
    buscarProductoPorNombre,
    actualizarProducto,
    eliminarProducto
)


# --- Funciones de utilidad ---
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_encabezado(titulo):
    print("\n" + "="*80)
    print(f"{titulo:^80}")
    print("="*80)


# --- PANTALLA 1: GESTION DE CLIENTES Y SUSCRIPCIONES --- 
def mostrarTablaClientes(datos):
    # 0:nombre, 1:apellido, 2:id, 3:tel, 4:email
    nombre_completo = f"{datos[0]} {datos[1]}"
    cedula = datos[2]
    telefono = datos[3]
    email = datos[4]
    
    # 5:sus_id, 6:frec, 7:fecha, 8:estado, 9:direccion
    sus_id = datos[5]
    frecuencia = f"{datos[6]} dias" if datos[6] else "N/A"
    fecha_prox = str(datos[7]) if datos[7] else "N/A"
    estado_sus = datos[8] if datos[8] else "Inactiva"
    
    # Si no tiene suscripcion, saldrá "No registrada"
    direccion = datos[9] if datos[9] else "No registrada"
    
    # --- Mostrar el cliente ---
    print("\n")
    print(f"{' DATOS DEL CLIENTE':<40} | {' SUSCRIPCIONES ACTIVAS':<40}")
    print("-" * 80)
    print(f" Nombre:    {nombre_completo:<28} |  ID Suscripcion: {str(sus_id) if sus_id else '---':<20}")
    print(f" Cedula:    {cedula:<28} |  Frecuencia:     {frecuencia:<20}")
    print(f" Direccion: {direccion:<28} |  Prox. Entrega:  {fecha_prox:<20}")
    print(f" Telefono:  {telefono:<28} |  Estado:         {estado_sus:<20}")
    print(f" Email:     {email:<28} |")
    print("-" * 80)

    return sus_id  # Retornamos el ID de la suscripcion (o None si no tiene)

def pantallaEditarCliente(cedula, datosAct):
    print("\n--- EDITAR INFORMACION ---")
    print("(Deje vacio y presione Enter para mantener el valor actual)")
    
    # Extraemos valores actuales
    # datos_actuales[0] es nombre, [1] es apellido, [3] telefono, [4] email
    n_nombre = input(f"Nombre [{datosAct[0]}]: ") or datosAct[0]
    n_apellido = input(f"Apellido [{datosAct[1]}]: ") or datosAct[1]
    n_telefono = input(f"Telefono [{datosAct[3]}]: ") or datosAct[3]
    n_email = input(f"Email [{datosAct[4]}]: ") or datosAct[4]
    
    if actualizarCliente(cedula, n_nombre, n_apellido, n_telefono, n_email):
        print("\nDatos actualizados correctamente.")
    else:
        print("\n[Error] No se pudo actualizar la informacion.")
    
    input("Presione ENTER para continuar...")

def pantallaGestionSuscripcion(cedula, sus_id):
    if sus_id:
        # Lógica de CANCELAR
        print(f"\n--- CANCELAR SUSCRIPCION #{sus_id} ---")
        confirmar = input("¿Esta seguro que desea cancelar esta suscripcion? (Sí = s / No = n): ")
        
        if confirmar.lower() == 's':
            if cancelarSuscripcion(sus_id):
                print("\nLa suscripcion ha sido cancelada.")
            else:
                print("\n[Error] No se pudo cancelar la suscripcion.")
        else:
            print("Operacion cancelada por el usuario.")
            
    else:
        # Lógica de CREAR
        print("\n--- NUEVA SUSCRIPCION ---")
        try:
            freq = int(input("Frecuencia (dias): "))
            prox = input("Fecha prox. entrega (YYYY-MM-DD): ")
            direc = input("Direccion de entrega: ")
            
            if crearSuscripcion(cedula, freq, direc, prox):
                print("\nSuscripcion creada exitosamente.")
            else:
                print("\n[Error] No se pudo crear la suscripcion.")
        except ValueError:
            print("\n[Error] La frecuencia debe ser un numero entero.")
    
    input("Presione ENTER para continuar...")

def pantalla1_GestionClientesSuscripciones():
    while True:
        #limpiar_pantalla()
        mostrar_encabezado("GESTION DE CLIENTES Y SUSCRIPCIONES")
        
        cedula_input = input("\nIngrese la Cedula del Cliente a buscar o escriba '1' para Salir: ")

        if cedula_input == '1':
            return
        
        datos = buscarClienteSuscripcion(cedula_input)
        
        if datos:
            while True:
                sus_id = mostrarTablaClientes(datos)            

                print("\nOPCINES DISPONIBLES:")
                print("1. Editar informacion del cliente")
                if sus_id:  # Si tiene suscripcion activa (sus_id no es None)
                    print("2. Cancelar suscripcion")
                else:
                    print("2. Crear nueva suscripcion")
                print("3. Nueva busqueda")
                print("4. Regresar al Menu Principal")

                opcion = input("\nSeleccione la opción que desea realizar: ")

                match opcion:
                    case "1":
                        pantallaEditarCliente(cedula_input, datos)
                        datos = buscarClienteSuscripcion(cedula_input)

                    case "2":
                        pantallaGestionSuscripcion(cedula_input, sus_id)
                        datos = buscarClienteSuscripcion(cedula_input)

                    case "3":
                        break

                    case "4":
                        return

                    case _:  # default
                        print("\n[!] Opcion inválida.")
                        input("Enter para intentar de nuevo...")

        else:
            print("\nCliente no encontrado en la base de datos.")
            retry = input("¿Desea buscar otro cliente? (Sí = s / No = n): ")
            if retry.lower() != 's':
                break


# --- PANTALLA 2: GESTION DE INVENTARIO ---
def mostrarTablaInventario(productos):
    # Encabezados
    print(f"{'ID':<5} {'Nombre':<25} {'Descripcion':<25} {'Precio':<10} {'Stock'}")
    print("-" * 80)
    
    for prod in productos:
        p_id = prod[0]
        nombre = prod[1]
        raw_desc = prod[2] if prod[2] else "---"
        
        ancho_desc = 25
        
        # 2. Si el texto es mas largo que el ancho, lo cortamos y ponemos "..."
        if len(raw_desc) > ancho_desc:
            # Cortamos 3 caracteres antes para que quepan los puntos suspensivos
            descripcion = raw_desc[:ancho_desc-3] + "..."
        else:
            descripcion = raw_desc
        # ----------------------------------

        precio = f"${prod[3]:.2f}"
        stock = prod[4]
        disponible = str(stock) if stock > 0 else "0"
        
        # Ahora imprimimos usando la variable 'descripcion' ya recortada
        print(f"{p_id:<5} {nombre:<25} {descripcion:<25} {precio:<10} {disponible}")
    
    print("-" * 80)

def pantallaAgregarProducto():
    print("\n--- AGREGAR NUEVO JUGO ---")
    try:
        nombre = input("Nombre del Jugo: ")
        desc = input("Descripcion: ")
        precio = float(input("Precio Unitario ($): "))
        stock = int(input("Stock Inicial: "))
        prov_id = input("ID Proveedor (Enter para default '1'): ") or "1"
        
        if crearProducto(nombre, desc, precio, stock, int(prov_id)):
            print("\nJugo agregado exitosamente al inventario.")
        else:
            print("\n[Error] No se pudo guardar el producto.")
            
    except ValueError:
        print("\n[Error] Precio y Stock deben ser numeros validos.")
    
    input("Presione ENTER para continuar...")

def pantallaActualizarProducto():
    print("\n--- ACTUALIZAR DATOS DEL JUGO ---")
    
    print("¿Por cuál vía desea buscar el jugo?")
    print("1. Por ID")
    print("2. Por Nombre")
    metodo_busqueda = input("Seleccione una opcion: ")
    
    prod_actual = None
    
    # Bloque de decisión: por ID o por Nombre
    if metodo_busqueda == "1":
        id_prod = input("Ingrese el ID del jugo: ").strip()
        prod_actual = buscarProductoPorId(id_prod)

    elif metodo_busqueda == "2":
        nombre_prod = input("Ingrese el nombre exacto del jugo: ").strip()
        prod_actual = buscarProductoPorNombre(nombre_prod)

    else:
        print("\n[!] Opcion no valida.")
        input("Enter para continuar...")
        return

    # Si encontramos el producto (por cualquiera de las dos vias)
    if prod_actual:
        # Importante: Para el UPDATE SQL necesitamos el ID. 
        # Lo sacamos de la tupla resultado (posición 0)
        id_para_actualizar = prod_actual[0]
        
        print(f"\nEditando: {prod_actual[1]} (ID: {id_para_actualizar})")
        print("(Deje vacio y presione Enter para mantener el valor actual)")
        
        try:
            # 1. Nombre
            n_nombre = input(f"Nombre [{prod_actual[1]}]: ") or prod_actual[1]
            
            # 2. Descripcion
            n_desc = input(f"Descripcion [{prod_actual[2]}]: ") or prod_actual[2]
            
            # 3. Precio
            input_precio = input(f"Precio [${prod_actual[3]}]: ")
            n_precio = float(input_precio) if input_precio else prod_actual[3]
            
            # 4. Stock
            input_stock = input(f"Stock [{prod_actual[4]}]: ")
            n_stock = int(input_stock) if input_stock else prod_actual[4]
            
            # Ejecutamos la actualizacion usando el ID que recuperamos
            if actualizarProducto(id_para_actualizar, n_nombre, n_desc, n_precio, n_stock):
                print("\nInventario actualizado correctamente.")
            else:
                print("\n[Error] No se pudo actualizar.")
                
        except ValueError:
            print("\n[Error] Precio y Stock deben ser valores numericos.")
    else:
        print("\nProducto no encontrado.")
        
    input("Presione ENTER para continuar...")

def pantallaEliminarProducto():
    print("\n--- ELIMINAR JUGO DEL INVENTARIO ---")
    
    print("¿Cómo desea buscar el jugo a eliminar?")
    print("1. Por ID")
    print("2. Por Nombre")
    metodo_busqueda = input("Seleccione una opcion: ")
    
    prod_encontrado = None
    
    # --- BLOQUE DE BÚSQUEDA (como en Actualizar) ---
    if metodo_busqueda == "1":
        id_prod = input("Ingrese el ID del jugo: ").strip()
        prod_encontrado = buscarProductoPorId(id_prod)
        
    elif metodo_busqueda == "2":
        nombre_prod = input("Ingrese el nombre del jugo: ").strip()
        prod_encontrado = buscarProductoPorNombre(nombre_prod)
        
    else:
        print("\n[!] Opcion no valida.")
        input("Enter para continuar...")
        return

    # --- BLOQUE DE CONFIRMACIÓN Y BORRADO ---
    if prod_encontrado:
        # Extraemos datos para mostrar advertencia
        # prod_encontrado es: (id, nombre, descripcion, precio, stock)
        id_a_borrar = prod_encontrado[0]
        nombre_a_borrar = prod_encontrado[1]
        
        print(f"\n[PELIGRO] Ha seleccionado: '{nombre_a_borrar}' (ID: {id_a_borrar})")
        print("ADVERTENCIA: Esta accion borrara el producto permanentemente.")
        
        confirmacion = input("¿Confirmar eliminacion? (Escriba exactamente 'si' para borrar): ")
        
        if confirmacion.lower() == "si":
            if eliminarProducto(id_a_borrar):
                print("\nProducto eliminado correctamente.")
            else:
                print("\n[Error] No se pudo eliminar (verifique si tiene ventas históricas asociadas).")
        else:
            print("\nOperacion cancelada por el usuario.")
            
    else:
        print("\nNo se encontro ningun producto con esos datos.")
    
    input("Presione ENTER para continuar...")

def pantalla2_GestionInventario():
    while True:
        #limpiar_pantalla()
        mostrar_encabezado("GESTION DE INVENTARIOS")
        
        productos = obtenerProductos()
        
        if productos:
            mostrarTablaInventario(productos)
        else:
            print("\nNo hay productos registrados o error de conexion.")

        print("\nOPCIONES DISPONIBLES:")
        print("1. Agregar nuevo Jugo")
        print("2. Actualizar Jugo")
        print("3. Eliminar Jugo")
        print("4. Regresar al Menu Principal")
        
        opcion = input("\nSeleccione la opcion que desea realizar: ")
        
        match opcion:
            case "1":
                pantallaAgregarProducto()
            
            case "2":
                pantallaActualizarProducto()
            
            case "3":
                pantallaEliminarProducto()
            
            case "4":
                return 
            
            case _:
                print("\n[!] Opcion invalida.")
                input("Enter para intentar de nuevo...")


# --- PANTALLA DEL MENÚ PRINCIPAL (Aquí se ejecuta todo el flujo del programa) ---
def main():
    while True:
        #limpiar_pantalla()
        print("\n" + "="*50)
        print(f"{' SISTEMA DE GESTION FRUTALIZATE':^50}")
        print("="*50)
        
        print("1. Gestion de Clientes y Suscripciones")
        print("2. Gestion de Inventario")
        print("3. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        # match es equivalente a switch-case
        match opcion:
            case "1":
                pantalla1_GestionClientesSuscripciones()
            
            case "2":
                pantalla2_GestionInventario()

            case "3":
                print("\nSaliendo del sistema...")
                break
            
            case _:  # Esto equivale al 'default'
                print("\n[!] Opcion inválida.")
                input("Enter para intentar de nuevo...")



# --- EJECUCION DEL PROGRAMA ---
if __name__ == "__main__":
    main()
