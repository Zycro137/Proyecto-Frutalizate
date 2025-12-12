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
    sql = "SELECT producto_id, nombre, precioUnitario, stock FROM Producto WHERE producto_id = %s"
    
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

def actualizarStockPrecio(id_producto, nuevo_precio, nuevo_stock):
    conexion = conectarBD()
    if not conexion:
        return False
    
    cursor = conexion.cursor()
    sql = "UPDATE Producto SET precioUnitario = %s, stock = %s WHERE producto_id = %s"
    
    try:
        cursor.execute(sql, (nuevo_precio, nuevo_stock, id_producto))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar producto: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()