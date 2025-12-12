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
    actualizarStockPrecio
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

def pantalla1_GestionClientes():
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



# --- MAIN (La función donde se ejecuta todo el flujo del programa) ---
def main():
    while True:
        #limpiar_pantalla()
        print("\n" + "="*50)
        print(f"{' SISTEMA DE GESTION FRUTALIZATE':^50}")
        print("="*50)
        
        print("1. Gestion de Clientes y Suscripciones")
        print("2. Gestion de Inventario")
        print("3. Salir")
        
        opcion = input("\nSeleccione una opcion: ")
        
        # match es equivalente a switch-case
        match opcion:
            case "1":
                pantalla1_GestionClientes()
            
            case "2":
                print("\nModulo 'Nuevo Pedido' en desarrollo.")
                input("Enter para continuar...")

            case "3":
                print("\nSaliendo del sistema...")
                break
            
            case _:  # Esto equivale al 'default'
                print("\n[!] Opcion inválida.")
                input("Enter para intentar de nuevo...")



# --- EJECUCION DEL PROGRAMA ---
if __name__ == "__main__":
    main()
