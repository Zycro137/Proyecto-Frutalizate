from src.controladores import pedidos, reportes, inventario
from src.conexion import conectarBD

conexion = conectarBD()

if conexion:
    cursor = conexion.cursor()
    

    # Cerrar es responsabilidad del flujo principal
    cursor.close()
    conexion.close()
    print("Conexion cerrada")
