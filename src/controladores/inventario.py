from src.conexion import conectarBD

def obtenerProductos():
    conexion = conectarBD()
    if not conexion:
        return []
    
    cursor = conexion.cursor()
    # Usamos la descripcion como 'Categoria' para el prototipo
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

def crearProducto(nombre, descripcion, precio, stock, proveedor_id):
    conexion = conectarBD()
    if not conexion:
        return False
    
    cursor = conexion.cursor()
    sql = """
    INSERT INTO Producto (nombre, descripcion, precioUnitario, stock, proveedor_id)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(sql, (nombre, descripcion, precio, stock, proveedor_id))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al crear producto: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def buscarProductoPorId(id_producto):
    conexion = conectarBD()
    if not conexion:
        return None
        
    cursor = conexion.cursor()
    sql = "SELECT producto_id, nombre, descripcion, precioUnitario, stock FROM Producto WHERE producto_id = %s"
    
    try:
        cursor.execute(sql, (id_producto,))
        producto = cursor.fetchone()
        return producto
    except Exception as e:
        print(f"Error al buscar producto: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def buscarProductoPorNombre(nombre):
    conexion = conectarBD()
    if not conexion:
        return None
    
    cursor = conexion.cursor()
    
    sql = "SELECT producto_id, nombre, descripcion, precioUnitario, stock FROM Producto WHERE LOWER(nombre) = LOWER(%s)"
    
    try:
        cursor.execute(sql, (nombre.strip(),))
        producto = cursor.fetchone()
        return producto
    except Exception as e:
        print(f"Error al buscar producto por nombre: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def actualizarProducto(id_producto, nombre, descripcion, precio, stock):
    conexion = conectarBD()
    if not conexion:
        return False
    
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
    if not conexion:
        return False
    
    cursor = conexion.cursor()
    # Sentencia SQL para borrar
    sql = "DELETE FROM Producto WHERE producto_id = %s"
    
    try:
        cursor.execute(sql, (id_producto,))
        conexion.commit()
        
        # cursor.rowcount nos dice cuantas filas fueron afectadas
        # Si es mayor a 0, significa que si borro algo
        if cursor.rowcount > 0:
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error al eliminar producto: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()
