import os
from src.controladores import pedidos, reportes, inventario
from src.conexion import conectarBD
from src.controladores.clientes import buscarClienteSuscripcion


def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_encabezado(titulo):
    print("\n" + "="*80)
    print(f"{titulo:^80}")
    print("="*80)

def pantalla_GestionClientes():
    while True:
        #limpiar_pantalla()
        mostrar_encabezado("GESTION DE CLIENTES Y SUSCRIPCIONES")
        
        cedula_input = input("\nIngrese la Cedula del Cliente a buscar: ")
        
        datos = buscarClienteSuscripcion(cedula_input)
        
        if datos:
            sus_id = mostrarTablaClientes(datos)            

            while True:
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
                        print("\nFuncion Editar Cliente aun no implementada.")
                        input("Presione ENTER para continuar...")

                    case "2":
                        print("\nFuncion Gestion Suscripcion aun no implementada.")
                        input("Presione ENTER para continuar...")

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
                pantalla_GestionClientes()
            
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
