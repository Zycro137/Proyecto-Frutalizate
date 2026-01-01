from src.conexion import conectarBD

# --- FUNCIONES DE LECTURA ---

def obtenerFrutas():
    """Retorna la lista de materia prima con su proveedor"""
    conexion = conectarBD()
    if not conexion: return []
    cursor = conexion.cursor()
    
    sql = """
    SELECT f.frutas_id, f.nombre, f.stock, p.nombre 
    FROM Frutas f
    JOIN Proveedor p ON f.proveedor_id = p.proveedor_id
    """
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error obteniendo frutas: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def obtenerProductos():
    """Retorna lista de Jugos (Productos terminados)"""
    conexion = conectarBD()
    if not conexion: return []
    cursor = conexion.cursor()
    
    sql = "SELECT producto_id, nombre, descripcion, precioUnitario, stock FROM Producto"
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al listar productos: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def buscarProductoPorId(id_producto):
    conexion = conectarBD()
    if not conexion: return None
    cursor = conexion.cursor()
    sql = "SELECT producto_id, nombre, descripcion, precioUnitario, stock FROM Producto WHERE producto_id = %s"
    try:
        cursor.execute(sql, (id_producto,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error al buscar producto: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def buscarProductoPorNombre(nombre):
    conexion = conectarBD()
    if not conexion: return None
    cursor = conexion.cursor()
    sql = "SELECT producto_id, nombre, descripcion, precioUnitario, stock FROM Producto WHERE LOWER(nombre) = LOWER(%s)"
    try:
        cursor.execute(sql, (nombre.strip(),))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error al buscar producto por nombre: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

# --- FUNCIONES DE ESCRITURA (JUGOS) ---

def crearProducto(nombre, descripcion, precio, stock, proveedor_id):
    conexion = conectarBD()
    if not conexion: return False
    cursor = conexion.cursor()
    
    sql = """
    INSERT INTO Producto (nombre, descripcion, precioUnitario, stock)
    VALUES (%s, %s, %s, %s)
    """
  
    try:
        cursor.execute(sql, (nombre, descripcion, precio, stock))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al crear producto: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def actualizarProducto(id_producto, nombre, descripcion, precio, stock):
    conexion = conectarBD()
    if not conexion: return False
    cursor = conexion.cursor()
    sql = """
    UPDATE Producto 
    SET nombre = %s, descripcion = %s, precioUnitario = %s, stock = %s 
    WHERE producto_id = %s
    """
    try:
        cursor.execute(sql, (nombre, descripcion, precio, stock, id_producto))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar producto: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def eliminarProducto(id_producto):
    conexion = conectarBD()
    if not conexion: return False
    cursor = conexion.cursor()
    sql = "DELETE FROM Producto WHERE producto_id = %s"
    try:
        cursor.execute(sql, (id_producto,))
        conexion.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error al eliminar producto (Puede tener pedidos asociados): {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()