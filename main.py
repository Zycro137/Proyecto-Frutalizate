import os
from src.controladores.clientes import (
    buscarClienteSuscripcion, 
    actualizarCliente, 
    crearSuscripcion, 
    cancelarSuscripcion
)
# (Manten tus imports de inventario igual)...
from src.controladores.inventario import (
    obtenerProductos, obtenerFrutas, crearProducto, buscarProductoPorId,
    buscarProductoPorNombre, actualizarProducto, eliminarProducto
)

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_encabezado(titulo):
    print("\n" + "="*80)
    print(f"{titulo:^80}")
    print("="*80)

# --- PANTALLA 1: MODIFICADA --- 

def mostrarTablaClientes(datos):
    # indices: 0:nom, 1:ape, 2:id, 3:tel, 4:email, 5:sus_id, 6:frec, 7:fecha, 8:estado
    nombre_completo = f"{datos[0]} {datos[1]}"
    cedula = datos[2]
    telefono = datos[3]
    email = datos[4]
    
    sus_id = datos[5]
    frecuencia = f"{datos[6]} dias" if datos[6] else "N/A"
    fecha_prox = str(datos[7]) if datos[7] else "N/A"
    estado_sus = datos[8] if datos[8] else "Inactiva"
    
    print("\n")
    print(f"{' DATOS DEL CLIENTE':<40} | {' ESTADO DE SUSCRIPCION':<40}")
    print("-" * 80)
    print(f" Nombre:    {nombre_completo:<28} |  ID Suscripcion: {str(sus_id) if sus_id else '---':<20}")
    print(f" Cedula:    {cedula:<28} |  Frecuencia:     {frecuencia:<20}")
    print(f" Telefono:  {telefono:<28} |  Prox. Entrega:  {fecha_prox:<20}")
    print(f" Email:     {email:<28} |  Estado:         {estado_sus:<20}")
    print("-" * 80)

    # CAMBIO: Retornamos el ID y tambien el ESTADO para validar en el menu
    return sus_id, estado_sus

def pantallaEditarCliente(cedula, datosAct):
    # (Esta funcion queda igual a la anterior, solo copiala aqui)
    print("\n--- EDITAR INFORMACION ---")
    print("(Deje vacio y presione Enter para mantener el valor actual)")
    n_nombre = input(f"Nombre [{datosAct[0]}]: ") or datosAct[0]
    n_apellido = input(f"Apellido [{datosAct[1]}]: ") or datosAct[1]
    n_telefono = input(f"Telefono [{datosAct[3]}]: ") or datosAct[3]
    n_email = input(f"Email [{datosAct[4]}]: ") or datosAct[4]
    
    if actualizarCliente(cedula, n_nombre, n_apellido, n_telefono, n_email):
        print("\nDatos actualizados correctamente.")
    else:
        print("\n[Error] No se pudo actualizar.")
    input("Presione ENTER para continuar...")

def pantallaGestionSuscripcion(cedula, sus_id, es_activa):
    """
    Gestiona tanto la creacion como la cancelacion dependiendo del estado.
    """
    
    # CASO 1: Si existe y esta ACTIVA -> Ofrecemos CANCELAR
    if sus_id and es_activa:
        print(f"\n--- CANCELAR SUSCRIPCION ACTIVA #{sus_id} ---")
        confirmar = input("¿Desea cancelar esta suscripcion? (Si = s / No = n): ")
        
        if confirmar.lower() == 's':
            if cancelarSuscripcion(sus_id):
                print("\nLa suscripcion ha sido cancelada exitosamente.")
            else:
                print("\n[Error] No se pudo cancelar.")
        else:
            print("Operacion cancelada.")
            
    # CASO 2: No existe O esta Cancelada -> Ofrecemos CREAR (REACTIVAR)
    else:
        titulo = "REACTIVAR SUSCRIPCION" if sus_id else "NUEVA SUSCRIPCION"
        print(f"\n--- {titulo} ---")
        print("Escriba 'SALIR' para volver atras.")
        
        try:
            freq = input("Frecuencia (dias): ")
            if freq.strip().upper() == "SALIR": return
            
            prox = input("Fecha prox. entrega (YYYY-MM-DD): ")
            if prox.strip().upper() == "SALIR": return
            
            if crearSuscripcion(cedula, int(freq), prox):
                print("\nSuscripcion creada/reactivada exitosamente.")
            else:
                print("\n[Error] No se pudo crear la suscripcion.")
        except ValueError:
            print("\n[Error] La frecuencia debe ser un numero.")
    
    input("Presione ENTER para continuar...")

def pantalla1_GestionClientesSuscripciones():
    while True:
        limpiar_pantalla()
        mostrar_encabezado("GESTION DE CLIENTES Y SUSCRIPCIONES")
        
        cedula_input = input("\nIngrese la Cedula del Cliente a buscar o escriba '1' para Salir: ")

        if cedula_input == '1': return
        
        datos = buscarClienteSuscripcion(cedula_input)
        
        if datos:
            while True:
                # Recuperamos ID y ESTADO
                sus_id, estado = mostrarTablaClientes(datos)            
                
                # LOGICA NUEVA:
                # Consideramos "Activa" solo si tiene ID Y el estado no es 'Cancelada'
                es_suscripcion_activa = (sus_id is not None) and (estado != 'Cancelada')

                print("\nOPCIONES DISPONIBLES:")
                print("1. Editar informacion del cliente")
                
                # El texto de la opcion 2 cambia dinamicamente
                if es_suscripcion_activa:
                    print("2. Cancelar suscripcion")
                else:
                    print("2. Suscribir cliente")
                    
                print("3. Nueva búsqueda")
                print("4. Regresar al Menú Principal")

                opcion = input("\nSeleccione la opción que desea realizar: ")

                match opcion:
                    case "1":
                        pantallaEditarCliente(cedula_input, datos)
                        datos = buscarClienteSuscripcion(cedula_input)
                    case "2":
                        # Pasamos el flag 'es_suscripcion_activa' para saber que hacer dentro
                        pantallaGestionSuscripcion(cedula_input, sus_id, es_suscripcion_activa)
                        datos = buscarClienteSuscripcion(cedula_input)
                    case "3":
                        break
                    case "4":
                        return
                    case _:
                        print("\n[!] Opcion invalida.")
                        input("Enter para intentar de nuevo...")
        else:
            print("\nCliente no encontrado.")
            retry = input("¿Buscar otro? (Si = s / No = n): ")
            if retry.lower() != 's': break


# --- PANTALLA 2: GESTION DE INVENTARIO ---

def mostrarTablaFrutas(frutas):
    mostrar_encabezado("INVENTARIO DE FRUTAS")
    print(f"\n{'ID':<5} {'Fruta':<15} {'Stock':<10} {'Proveedor':<25}")
    print("-" * 60)
    for f in frutas:
        # f = (id, nombre, stock, proveedor)
        print(f"{f[0]:<5} {f[1]:<15} {f[2]:<10} {f[3]:<25}")
    print("-" * 60)

def mostrarTablaInventario(productos):
    print(f"\n{'ID':<5} {'Nombre':<25} {'Descripcion':<25} {'Precio':<10} {'Stock'}")
    print("-" * 80)
    for prod in productos:
        p_id = prod[0]
        nombre = prod[1]
        raw_desc = prod[2] if prod[2] else "---"
        
        ancho_desc = 25
        if len(raw_desc) > ancho_desc:
            descripcion = raw_desc[:ancho_desc-3] + "..."
        else:
            descripcion = raw_desc

        precio = f"${prod[3]:.2f}"
        stock = prod[4]
        disponible = str(stock) if stock > 0 else "0"
        
        print(f"{p_id:<5} {nombre:<25} {descripcion:<25} {precio:<10} {disponible}")
    print("-" * 80)

def pantallaAgregarProducto():
    print("\n--- AGREGAR NUEVO JUGO ---")
    print("En cualquier momento escriba 'SALIR' para cancelar.")
    try:
        nombre = input("Nombre del Jugo: ")
        if nombre.strip().upper() == "SALIR": return
        
        desc = input("Descripcion: ")
        if desc.strip().upper() == "SALIR": return
        
        precio = input("Precio Unitario ($): ")
        if precio.strip().upper() == "SALIR": return
        
        stock = input("Stock Inicial: ")
        if stock.strip().upper() == "SALIR": return
        
        # En la BD actual, Proveedor esta ligado a Frutas, no a Producto directo, 
        # pero mantenemos el input por si se requiere logica futura.
        prov_id = input("ID Proveedor (opcional): ") 
        if prov_id.strip().upper() == "SALIR": return
        
        if crearProducto(nombre, desc, float(precio), int(stock), prov_id):
            print("\nJugo agregado exitosamente.")
        else:
            print("\n[Error] No se pudo guardar el producto.")
            
    except ValueError:
        print("\n[Error] Precio y Stock deben ser numeros validos.")
    
    input("Presione ENTER para continuar...")

def pantallaActualizarProducto():
    print("\n--- ACTUALIZAR DATOS DEL JUGO ---")
    print("1. Por ID")
    print("2. Por Nombre")
    metodo = input("Seleccione: ")
    
    prod_actual = None
    if metodo == "1":
        id_prod = input("ID del jugo: ").strip()
        prod_actual = buscarProductoPorId(id_prod)
    elif metodo == "2":
        nombre = input("Nombre del jugo: ").strip()
        prod_actual = buscarProductoPorNombre(nombre)
    else:
        print("\n[!] Opcion no valida.")
        input("Enter para continuar...")
        return

    if prod_actual:
        id_para_act = prod_actual[0]
        print(f"\nEditando: {prod_actual[1]} (ID: {id_para_act})")
        print("(Deje vacio y Enter para mantener valor actual)")
        
        try:
            n_nombre = input(f"Nombre [{prod_actual[1]}]: ") or prod_actual[1]
            n_desc = input(f"Descripcion [{prod_actual[2]}]: ") or prod_actual[2]
            
            in_precio = input(f"Precio [${prod_actual[3]}]: ")
            n_precio = float(in_precio) if in_precio else prod_actual[3]
            
            in_stock = input(f"Stock [{prod_actual[4]}]: ")
            n_stock = int(in_stock) if in_stock else prod_actual[4]
            
            if actualizarProducto(id_para_act, n_nombre, n_desc, n_precio, n_stock):
                print("\nInventario actualizado.")
            else:
                print("\n[Error] No se pudo actualizar.")
        except ValueError:
            print("\n[Error] Valores numericos invalidos.")
    else:
        print("\nProducto no encontrado.")
    
    input("Enter para continuar...")

def pantallaEliminarProducto():
    print("\n--- ELIMINAR JUGO ---")
    print("1. Por ID")
    print("2. Por Nombre")
    metodo = input("Seleccione: ")
    
    prod = None
    if metodo == "1":
        i = input("ID: ").strip()
        prod = buscarProductoPorId(i)
    elif metodo == "2":
        n = input("Nombre: ").strip()
        prod = buscarProductoPorNombre(n)
    
    if prod:
        print(f"\n[PELIGRO] Eliminando: '{prod[1]}' (ID: {prod[0]})")
        conf = input("Escriba 'si' para borrar: ")
        if conf.lower() == "si":
            if eliminarProducto(prod[0]):
                print("\nProducto eliminado.")
            else:
                print("\n[Error] No se pudo eliminar.")
        else:
            print("\nCancelado.")
    else:
        print("\nNo encontrado.")
    
    input("Enter para continuar...")

def pantalla2_GestionInventario():
    while True:
        limpiar_pantalla()
        mostrar_encabezado("GESTION DE INVENTARIOS")
        
        print("¿Qué acción desea realizar?")
        print("1. Consultar inventario de Frutas")
        print("2. Gestionar inventario de Jugos")
        print("3. Regresar al Menu Principal")
        
        tipo_inv = input("\nOpción seleccionada: ")
        
        if tipo_inv == "1":
            # GESTION FRUTAS (Solo lectura en este prototipo)
            limpiar_pantalla()
            frutas = obtenerFrutas()
            if frutas:
                mostrarTablaFrutas(frutas)
            else:
                print("\nNo hay frutas registradas.")
            input("\nPresione ENTER para volver...")
            
        elif tipo_inv == "2":
            # GESTION JUGOS
            while True:
                limpiar_pantalla()
                mostrar_encabezado("GESTION DE JUGOS")
                
                productos = obtenerProductos()
                if productos:
                    mostrarTablaInventario(productos)
                else:
                    print("\nNo hay jugos registrados.")

                print("\nOPCIONES JUGOS:")
                print("1. Agregar Jugo")
                print("2. Actualizar Jugo")
                print("3. Eliminar Jugo")
                print("4. Volver a seleccion de inventario")
                
                opc = input("\nSeleccione: ")
                
                if opc == "1": pantallaAgregarProducto()
                elif opc == "2": pantallaActualizarProducto()
                elif opc == "3": pantallaEliminarProducto()
                elif opc == "4": break
                else: 
                    print("Invalido")
                    input("Enter...")
                    
        elif tipo_inv == "3":
            return
        else:
            print("Opcion invalida")
            input("Enter...")

# --- MENU PRINCIPAL ---
def main():
    while True:
        limpiar_pantalla()
        print("\n" + "="*50)
        print(f"{' SISTEMA DE GESTION FRUTALIZATE':^50}")
        print("="*50)
        
        print("1. Gestion de Clientes y Suscripciones")
        print("2. Gestion de Inventarios")
        print("3. Salir")
        
        opcion = input("\nSeleccione una opcion: ")
        
        match opcion:
            case "1":
                pantalla1_GestionClientesSuscripciones()
            case "2":
                pantalla2_GestionInventario()
            case "3":
                print("\nSaliendo del sistema...")
                break
            case _:
                print("\n[!] Opcion invalida.")
                input("Enter para intentar de nuevo...")

if __name__ == "__main__":
    main()