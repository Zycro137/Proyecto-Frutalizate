import os
import sys

# --- IMPORTAMOS TODOS LOS CONTROLADORES ---
from src.controladores.clientes import (
    buscarClienteSuscripcion, 
    actualizarCliente, 
    crearSuscripcion, 
    cancelarSuscripcion,
    obtenerClientes,
    crearCliente,
    eliminarCliente,
    obtenerTodasSuscripciones,
    actualizarSuscripcion,
    eliminarSuscripcionFisica,
    obtenerSuscripcionPorId,
    obtenerReporteSuscripcionesVista
)

from src.controladores.inventario import (
    obtenerProductos,
    obtenerFrutas,
    crearProducto,
    buscarProductoPorId,
    buscarProductoPorNombre,
    actualizarProducto,
    eliminarProducto
)

from src.controladores.pedidos import (
    obtenerPedidos,
    obtenerRepartidores,
    obtenerDetallePedido,
    crearPedidoCompleto,
    actualizarEstadoPedido,
    eliminarPedido,
    obtenerReportePedidosCliente,
    obtenerReporteDetallePedido
)

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_encabezado(titulo):
    print("\n" + "="*80)
    print(f"{titulo:^80}")
    print("="*80)

# --- PANTALLA 1: DETALLES DE CLIENTES --- 

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

    return sus_id, estado_sus

def pantallaEditarCliente(cedula, datosAct):
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

def mostrarTablaTodosClientes(clientes):
    print(f"\n{'CEDULA':<15} {'NOMBRE':<20} {'APELLIDO':<20} {'TELEFONO':<15} {'EMAIL'}")
    print("-" * 90)
    for c in clientes:
        ced = c[0]
        nom = c[1]
        ape = c[2]
        tel = c[3] if c[3] else "---"
        mail = c[4] if c[4] else "---"
        print(f"{ced:<15} {nom:<20} {ape:<20} {tel:<15} {mail}")
    print("-" * 90)

def pantalla1_DetallesClientesSuscripciones():
    while True:
        limpiar_pantalla()
        mostrar_encabezado("DETALLES DE CLIENTES Y SUSCRIPCIONES")
        
        todos_los_clientes = obtenerClientes()
        if todos_los_clientes:
            mostrarTablaTodosClientes(todos_los_clientes)
        else:
            print("\n[!] No hay clientes registrados en el sistema.")
        
        cedula_input = input("\nIngrese la Cedula del Cliente a buscar o escriba '1' para Salir: ")
        if cedula_input == '1': return
        
        datos = buscarClienteSuscripcion(cedula_input)
        if datos:
            while True:
                sus_id, estado = mostrarTablaClientes(datos)            
                es_suscripcion_activa = (sus_id is not None) and (estado != 'Cancelada')

                print("\nOPCIONES DISPONIBLES:")
                print("1. Editar informacion del cliente")
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
                        pantallaGestionSuscripcion(cedula_input, sus_id, es_suscripcion_activa)
                        datos = buscarClienteSuscripcion(cedula_input)
                    case "3": break
                    case "4": return
                    case _: 
                        print("\n[!] Opcion invalida.")
                        input("Enter...")
        else:
            print("\nCliente no encontrado.")
            retry = input("¿Buscar otro? (Si = s / No = n): ")
            if retry.lower() != 's': break

# --- PANTALLA 2: GESTION DE TABLAS ---

def mostrarTablaFrutas(frutas):
    mostrar_encabezado("INVENTARIO DE FRUTAS")
    print(f"\n{'ID':<5} {'Fruta':<15} {'Stock':<10} {'Proveedor':<25}")
    print("-" * 60)
    for f in frutas:
        # Nota: f[3] ahora es nombre de proveedor dado que usamos la Vista
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
        if len(raw_desc) > ancho_desc: descripcion = raw_desc[:ancho_desc-3] + "..."
        else: descripcion = raw_desc
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
        prov_id = input("ID Proveedor (opcional): ")
        
        # Llama a la funcion que usa el Stored Procedure
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
            
            # Llama a SP updateProducto, aquí saltará el Trigger si stock < 0
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
                print("\n[Error] No se pudo eliminar (Posiblemente tiene pedidos asociados).")
        else:
            print("\nCancelado.")
    else:
        print("\nNo encontrado.")
    input("Enter para continuar...")

def pantallaGestionClientesAdmin():
    while True:
        limpiar_pantalla()
        mostrar_encabezado("GESTION DE CLIENTES")
        lista_clientes = obtenerClientes()
        if lista_clientes: mostrarTablaTodosClientes(lista_clientes)
        else: print("\nNo hay clientes registrados.")

        print("\nOPCIONES DISPONIBLES:")
        print("1. Registrar nuevo cliente")
        print("2. Actualizar datos de cliente")
        print("3. Eliminar cliente")
        print("4. Volver")
        opc = input("\nSeleccione una opcion: ")
        
        if opc == "1":
            print("\n--- NUEVO CLIENTE ---")
            c_ced = input("Cedula: ")
            c_nom = input("Nombre: ")
            c_ape = input("Apellido: ")
            c_tel = input("Telefono: ")
            c_mail = input("Email: ")
            if crearCliente(c_ced, c_nom, c_ape, c_tel, c_mail):
                print("\nCliente registrado exitosamente.")
            else:
                print("\n[Error] No se pudo registrar (verifique si la cedula ya existe).")
            input("Enter...")

        elif opc == "2":
            print("\n--- ACTUALIZAR CLIENTE ---")
            ced_buscar = input("Ingrese la cedula del cliente a editar: ")
            datos = buscarClienteSuscripcion(ced_buscar)
            if datos:
                print(f"Editando a: {datos[0]} {datos[1]}")
                print("(Deje vacio y Enter para mantener valor actual)")
                n_nom = input(f"Nombre [{datos[0]}]: ") or datos[0]
                n_ape = input(f"Apellido [{datos[1]}]: ") or datos[1]
                n_tel = input(f"Telefono [{datos[3]}]: ") or datos[3]
                n_mail = input(f"Email [{datos[4]}]: ") or datos[4]
                if actualizarCliente(ced_buscar, n_nom, n_ape, n_tel, n_mail):
                    print("\nCliente actualizado.")
                else: print("\nError al actualizar.")
            else: print("\nCliente no encontrado.")
            input("Enter...")

        elif opc == "3":
            print("\n--- ELIMINAR CLIENTE ---")
            ced_borrar = input("Ingrese la cedula del cliente a eliminar: ")
            datos = buscarClienteSuscripcion(ced_borrar)
            if datos:
                print(f"\n[PELIGRO] Va a eliminar a: {datos[0]} {datos[1]}")
                conf = input("Escriba 'si' para confirmar borrado: ")
                if conf.lower() == 'si':
                    # Llama a SP deleteCliente
                    if eliminarCliente(ced_borrar):
                        print("\nCliente eliminado correctamente.")
                    else:
                        print("\n[Error] No se pudo eliminar (Posiblemente tiene deudas/pedidos).")
                else: print("\nCancelado.")
            else: print("\nCliente no encontrado.")
            input("Enter...")

        elif opc == "4": break
        else:
            print("Opcion invalida.")
            input("Enter...")

def mostrarTablaSuscripciones(lista):
    print(f"\n{'ID':<5} {'CLIENTE':<30} {'FRECUENCIA':<12} {'PROX. ENTREGA':<15} {'ESTADO'}")
    print("-" * 90)
    for s in lista:
        s_id = s[0]
        cliente = f"{s[1]} {s[2]}"
        freq = f"{s[3]} dias"
        fecha = str(s[4])
        estado = s[5]
        print(f"{s_id:<5} {cliente:<30} {freq:<12} {fecha:<15} {estado}")
    print("-" * 90)

def pantallaGestionSuscripcionesAdmin():
    while True:
        limpiar_pantalla()
        mostrar_encabezado("GESTION DE SUSCRIPCIONES")
        suscripciones = obtenerTodasSuscripciones()
        if suscripciones: mostrarTablaSuscripciones(suscripciones)
        else: print("\nNo hay suscripciones registradas.")
        
        print("\nOPCIONES DISPONIBLES:")
        print("1. Crear nueva suscripcion")
        print("2. Modificar suscripcion")
        print("3. Eliminar suscripcion")
        print("4. Volver")
        opc = input("\nSeleccione una opcion: ")
        
        if opc == "1":
            print("\n--- NUEVA SUSCRIPCION ---")
            cedula = input("Ingrese Cedula del Cliente: ")
            datos_cliente = buscarClienteSuscripcion(cedula)
            if datos_cliente:
                print(f"Cliente seleccionado: {datos_cliente[0]} {datos_cliente[1]}")
                try:
                    freq = int(input("Frecuencia (dias): "))
                    prox = input("Fecha prox. entrega (YYYY-MM-DD): ")
                    if crearSuscripcion(cedula, freq, prox):
                        print("\nSuscripcion creada exitosamente.")
                    else: print("\nError al crear.")
                except ValueError: print("\nLa frecuencia debe ser numerica.")
            else: print("\nCliente no encontrado.")
            input("Enter...")

        elif opc == "2":
            print("\n--- MODIFICAR SUSCRIPCION ---")
            s_id = input("ID de Suscripcion a modificar: ")
            sus_actual = obtenerSuscripcionPorId(s_id)
            if sus_actual:
                print(f"\nEditando Suscripcion #{s_id}")
                print("(Solo presione Enter para mantener el valor actual)")
                try:
                    input_freq = input(f"Nueva Frecuencia [{sus_actual[0]} dias]: ")
                    n_freq = int(input_freq) if input_freq else sus_actual[0]
                    fecha_vieja = str(sus_actual[1])
                    input_fecha = input(f"Nueva Fecha [{fecha_vieja}]: ")
                    n_fecha = input_fecha or fecha_vieja
                    if actualizarSuscripcion(s_id, n_freq, n_fecha):
                        print("\nDatos actualizados correctamente.")
                    else: print("\nNo se pudo actualizar.")
                except ValueError: print("\n[Error] La frecuencia debe ser un numero entero.")
            else: print("\nID de suscripcion no encontrado.")
            input("Enter...")

        elif opc == "3":
            print("\n--- ELIMINAR SUSCRIPCION ---")
            s_id = input("ID de Suscripcion a eliminar: ")
            print("[ALERTA] Esto borrará el registro permanentemente.")
            conf = input("Escriba 'si' para confirmar: ")
            if conf.lower() == 'si':
                if eliminarSuscripcionFisica(s_id):
                    print("\nRegistro eliminado.")
                else: print("\n[Error] No se pudo eliminar.")
            else: print("Cancelado.")
            input("Enter...")
        elif opc == "4": break
        else:
            print("Opcion invalida.")
            input("Enter...")

def mostrarTablaPedidos(lista_pedidos):
    print(f"\n{'ID':<5} {'FECHA':<12} {'CLIENTE':<25} {'REPARTIDOR':<15} {'HORA':<10} {'ESTADO'}")
    print("-" * 90)
    for p in lista_pedidos:
        pid = p[0]
        fecha = str(p[1])
        hora = str(p[2])
        estado = p[3]
        cliente = f"{p[4]} {p[5]}"
        repartidor = p[6] if p[6] else "Sin asignar"
        print(f"{pid:<5} {fecha:<12} {cliente:<25} {repartidor:<15} {hora:<10} {estado}")
    print("-" * 90)

def pantallaGestionPedidosAdmin():
    while True:
        limpiar_pantalla()
        mostrar_encabezado("GESTION DE PEDIDOS")
        pedidos = obtenerPedidos()
        if pedidos: mostrarTablaPedidos(pedidos)
        else: print("\nNo hay pedidos registrados.")
            
        print("\nOPCIONES DISPONIBLES:")
        print("1. Registrar Nuevo Pedido")
        print("2. Ver detalles de un pedido")
        print("3. Actualizar Estado")
        print("4. Eliminar Pedido")
        print("5. Volver")
        opc = input("\nSeleccione una opcion: ")
        
        if opc == "1":
            print("\n--- PASO 1: ASIGNAR CLIENTE ---")
            cedula = input("Ingrese Cedula del Cliente: ")
            cliente = buscarClienteSuscripcion(cedula)
            if not cliente:
                print("Cliente no encontrado.")
                input("Enter...")
                continue
            print(f"Cliente: {cliente[0]} {cliente[1]}")
            
            carrito = [] 
            print("\n--- PASO 2: AGREGAR PRODUCTOS ---")
            while True:
                id_prod = input("\nID Producto a agregar (o 'F' para finalizar lista): ")
                if id_prod.upper() == 'F':
                    if len(carrito) > 0: break
                    else: 
                        print("Debe agregar al menos un producto.")
                        continue
                
                prod = buscarProductoPorId(id_prod)
                if prod:
                    print(f"Producto: {prod[1]} | Stock Actual: {prod[4]} | Precio: ${prod[3]}")
                    try:
                        cant = int(input("Cantidad: "))
                        # Mantenemos validacion visual para UX, pero la BD protege el stock real con Trigger
                        if cant <= prod[4]:
                            carrito.append((prod[0], cant, prod[3]))
                            print("Producto agregado al carrito.")
                        else:
                            print("Stock insuficiente (Validacion Local).")
                    except ValueError: print("Cantidad invalida.")
                else: print("Producto no existe.")
            
            print("\n--- PASO 3: DATOS DE ENTREGA ---")
            repartidores = obtenerRepartidores()
            print("\nRepartidores disponibles:")
            for r in repartidores: print(f"ID {r[0]}: {r[1]} {r[2]}")
            id_rep = input("ID Repartidor: ")
            direc = input("Direccion de entrega: ")
            hora = input("Hora de entrega (HH:MM:SS): ")
            
            # Llama a la nueva funcion que usa SP 'insertPedido' y Trigger
            if crearPedidoCompleto(cedula, id_rep, direc, hora, carrito):
                print("\n¡Pedido registrado exitosamente!")
            else:
                print("\nError al registrar el pedido.")
            input("Enter para continuar...")

        elif opc == "2":
            pid = input("\nIngrese ID del Pedido a consultar: ")
            detalles = obtenerDetallePedido(pid) 
            if detalles:
                print(f"\n--- Detalle del Pedido #{pid} ---")
                print(f"{'PRODUCTO':<20} {'CANT':<5} {'SUBTOTAL'}")
                total = 0
                for d in detalles:
                    print(f"{d[2]:<20} {d[0]:<5} ${d[1]:.2f}")
                    total += d[1]
                print("-" * 40)
                print(f"TOTAL PAGADO: ${total:.2f}")
            else: print("No se encontraron detalles o ID invalido.")
            input("Enter...")

        elif opc == "3":
            pid = input("\nID del Pedido: ")
            print("Estados: Pendiente, En Camino, Entregado, Cancelado")
            n_estado = input("Nuevo estado: ")
            if actualizarEstadoPedido(pid, n_estado): print("Estado actualizado.")
            else: print("Error al actualizar.")
            input("Enter...")

        elif opc == "4":
            pid = input("\nID del Pedido a eliminar: ")
            conf = input("Confirmar borrado (si/no): ")
            if conf.lower() == 'si':
                if eliminarPedido(pid): print("Pedido eliminado.")
                else: print("Error al eliminar.")
            input("Enter...")
        elif opc == "5": break
        else: print("Opcion invalida")


def pantalla2_GestionInventario():
    while True:
        limpiar_pantalla()
        mostrar_encabezado("GESTIÓN DE INVENTARIOS")
        
        print("¿Qué acción desea realizar?")
        print("1. Consultar inventario de Frutas")
        print("2. Gestionar inventario de Jugos")
        print("3. Gestionar clientes")
        print("4. Gestionar suscripciones")
        print("5. Gestionar pedidos")
        print("6. Regresar al Menu Principal")
        
        opcion = input("\nSeleccione una opción: ")
        
        match opcion:
            case "1":
                limpiar_pantalla()
                frutas = obtenerFrutas() # Llama a la Vista reporte_frutas
                if frutas: mostrarTablaFrutas(frutas)
                else: print("\nNo hay frutas registradas.")
                input("\nPresione ENTER para volver...")
            case "2":
                while True:
                    limpiar_pantalla()
                    mostrar_encabezado("GESTION DE JUGOS")
                    productos = obtenerProductos()
                    if productos: mostrarTablaInventario(productos)
                    else: print("\nNo hay jugos registrados.")
                    print("\nOPCIONES JUGOS:")
                    print("1. Agregar Jugo")
                    print("2. Actualizar Jugo")
                    print("3. Eliminar Jugo")
                    print("4. Volver a seleccion de inventario")
                    opc_jugos = input("\nSeleccione: ")
                    match opc_jugos:
                        case "1": pantallaAgregarProducto()
                        case "2": pantallaActualizarProducto()
                        case "3": pantallaEliminarProducto()
                        case "4": break
                        case _: 
                            print("Invalido")
                            input("Enter...")
            case "3": pantallaGestionClientesAdmin()
            case "4": pantallaGestionSuscripcionesAdmin()
            case "5": pantallaGestionPedidosAdmin()
            case "6": return
            case _:
                print("\nOpción inválida.")
                input("Enter para intentar de nuevo...")

# --- PANTALLA 3: REPORTES ---

def pantalla3_Reportes():
    while True:
        limpiar_pantalla()
        mostrar_encabezado("REPORTES DEL SISTEMA")
        print("Estos reportes consultan directamente las VISTAS creadas en la BD.")
        print("1. Reporte: Pedidos por Cliente")
        print("2. Reporte: Detalle de Productos Vendidos")
        print("3. Reporte: Materia Prima (Frutas)")
        print("4. Reporte: Suscripciones Activas con Detalles")
        print("5. Volver")
        
        opc = input("\nSeleccione reporte: ")
        
        if opc == "1":
            data = obtenerReportePedidosCliente()
            print(f"\n{'ID':<5} {'CLIENTE':<25} {'FECHA':<12} {'ESTADO':<10} {'TOTAL'}")
            print("-" * 70)
            for row in data:
                nom = f"{row[1]} {row[2]}"
                total = f"${row[6]}" if row[6] else "Pend."
                print(f"{row[0]:<5} {nom:<25} {str(row[3]):<12} {row[4]:<10} {total}")
            input("\nPresione ENTER para continuar...")

        elif opc == "2":
            data = obtenerReporteDetallePedido()
            print(f"\n{'PEDIDO':<8} {'PRODUCTO':<20} {'CANT':<5} {'SUBTOTAL'}")
            print("-" * 60)
            for row in data:
                print(f"{row[0]:<8} {row[1]:<20} {row[2]:<5} ${row[3]}")
            input("\nPresione ENTER para continuar...")

        elif opc == "3":
            data = obtenerFrutas()
            print(f"\n{'PRODUCTO':<25} {'FRUTA USADA':<15} {'STOCK DE FRUTA':<15} {'PROVEEDOR'}")
            print("-" * 80)
            for row in data:
                print(f"{row[0]:<25} {row[1]:<15} {row[3]:<15} {row[2]}")
            input("\nPresione ENTER para continuar...")

        elif opc == "4":
            data = obtenerReporteSuscripcionesVista()
            if not data: print("\n[Nota] Tabla vacía (Verifique 'Suscripcion_Detalle').")
            print(f"\n{'SUS_ID':<8} {'CLIENTE':<20} {'PRODUCTO':<15} {'FRECUENCIA'}")
            print("-" * 70)
            for row in data:
                nom = f"{row[1]} {row[2]}"
                print(f"{row[0]:<8} {nom:<20} {row[3]:<15} {row[5]} dias")
            input("\nPresione ENTER para continuar...")

        elif opc == "5": break

# --- MENU PRINCIPAL ---
def main():
    while True:
        limpiar_pantalla()
        mostrar_encabezado("SISTEMA DE GESTION FRUTALIZATE")
        
        print("1. Detalles de Clientes y Suscripciones")
        print("2. Gestion de Tablas")
        print("3. Reportes")
        print("4. Salir")
        
        opcion = input("\nSeleccione una opcion: ")
        
        match opcion:
            case "1":
                pantalla1_DetallesClientesSuscripciones()
            case "2":
                pantalla2_GestionInventario()
            case "3":
                pantalla3_Reportes()
            case "4":
                print("\nSaliendo del sistema...")
                break
            case _:
                print("\n[!] Opcion invalida.")
                input("Enter para intentar de nuevo...")

if __name__ == "__main__":
    main()