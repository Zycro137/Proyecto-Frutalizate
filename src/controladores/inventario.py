from src.conexion import conectarBD
import mysql.connector

# --- FUNCIONES DE LECTURA ---

def obtenerFrutas():
    """
    Retorna la lista de materia prima usando la VISTA creada por el Grupo 3.
    Vista: reporte_frutas
    """
    conexion = conectarBD()
    if not conexion: return []
    cursor = conexion.cursor()
    
    # ¡Mucho más limpio! Usamos la vista en lugar del JOIN manual
    sql = "SELECT * FROM reporte_frutas"
    
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
    """
    Retorna lista de Jugos. Mantenemos el SELECT simple ya que
    no hay una Vista especifica para 'todo el producto raw'.
    """
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

# --- FUNCIONES DE ESCRITURA (JUGOS) CON STORED PROCEDURES ---

def crearProducto(nombre, descripcion, precio, stock, proveedor_id=None):
    """
    Nota: El parámetro proveedor_id lo ignoramos porque el SP 'crearProducto' 
    solo pide (nombre, descripcion, precio, stock).
    """
    conexion = conectarBD()
    if not conexion: return False
    cursor = conexion.cursor()
    
    try:
        # SP: crearProducto(p_nombre, p_descripcion, p_precio, p_stock)
        cursor.callproc('crearProducto', [nombre, descripcion, precio, stock])
        conexion.commit()
        return True
        
    except mysql.connector.Error as err:
        print(f"Error BD: {err.msg}")
        return False
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
    
    try:
        # SP: updateProducto(p_id, p_nombre, p_desc, p_precio, p_stock)
        cursor.callproc('updateProducto', [id_producto, nombre, descripcion, precio, stock])
        conexion.commit()
        return True
        
    except mysql.connector.Error as err:
        # Aquí saltará el Trigger 'validar_stock_negativo_update' si stock < 0
        # err.msg contendrá: "Error: El stock del producto no puede ser negativo"
        print(f"Error BD: {err.msg}")
        return False
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
    
    try:
        # SP: deleteProducto(p_id)
        cursor.callproc('deleteProducto', [id_producto])
        conexion.commit()
        return True
        
    except mysql.connector.Error as err:
        # El SP ya valida si existe. Si hay integridad referencial (pedidos), saltará error estándar.
        print(f"Error BD: {err.msg}")
        return False
    except Exception as e:
        print(f"Error al eliminar producto: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()