from src.conexion import conectarBD

def obtener_todos_productos():
    conexion = conectarBD()
    if not conexion:
        return []
    
    cursor = conexion.cursor()
    
    # Seleccionamos columnas que coinciden con tu diseño visual
    # Usaremos 'descripcion' como Categoría
    sql = "SELECT producto_id, nombre, descripcion, precioUnitario, stock FROM Producto"
    
    try:
        cursor.execute(sql)
        productos = cursor.fetchall()
        return productos
    except Exception as e:
        print(f"Error al listar productos: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()