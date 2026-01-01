from datetime import date, datetime
from src.conexion import conectarBD

# --- LECTURAS ---

def obtenerPedidos():
    """Devuelve historial de pedidos con nombre de cliente y repartidor."""
    conexion = conectarBD()
    if not conexion: return []
    cursor = conexion.cursor()
    
    # Hacemos JOIN con Cliente y Repartidor para mostrar nombres reales
    sql = """
    SELECT 
        p.pedido_id,
        p.fechaRealizado,
        p.horaEntrega,
        p.estado,
        c.nombre,
        c.apellido,
        r.nombre
    FROM Pedido p
    JOIN Cliente c ON p.cliente_id = c.cliente_id
    LEFT JOIN Repartidor r ON p.repartidor_id = r.repartidor_id
    ORDER BY p.pedido_id DESC
    """
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al listar pedidos: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def obtenerRepartidores():
    """Lista simple para seleccionar repartidor al crear pedido."""
    conexion = conectarBD()
    if not conexion: return []
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT repartidor_id, nombre, apellido FROM Repartidor")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error repartidores: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def obtenerDetallePedido(id_pedido):
    """Obtiene los productos de un pedido especifico."""
    conexion = conectarBD()
    if not conexion: return []
    cursor = conexion.cursor()
    
    sql = """
    SELECT 
        dp.cantidad,
        dp.subtotal,
        prod.nombre
    FROM Detalle_Pedido dp
    JOIN Producto prod ON dp.producto_id = prod.producto_id
    WHERE dp.pedido_id = %s
    """
    try:
        cursor.execute(sql, (id_pedido,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al ver detalle: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

# CRUD PEDIDOS

def crearPedidoCompleto(cliente_id, repartidor_id, direccion, hora, lista_productos):
    """
    Inserta el Pedido Y sus Detalles en una sola transaccion.
    lista_productos es una lista de tuplas: (id_producto, cantidad, precio_unitario)
    """
    conexion = conectarBD()
    if not conexion: return False
    cursor = conexion.cursor()
    
    try:
        # 1. Insertar ENCABEZADO (Tabla Pedido)
        fecha_hoy = date.today()
        sql_encabezado = """
        INSERT INTO Pedido (fechaRealizado, horaEntrega, estado, direccion, cliente_id, repartidor_id)
        VALUES (%s, %s, 'Pendiente', %s, %s, %s)
        """
        cursor.execute(sql_encabezado, (fecha_hoy, hora, direccion, cliente_id, repartidor_id))
        
        # Recuperamos el ID generado automaticamente
        id_pedido_generado = cursor.lastrowid
        
        # 2. Insertar DETALLES (Tabla Detalle_Pedido) y DESCONTAR STOCK
        sql_detalle = """
        INSERT INTO Detalle_Pedido (cantidad, subtotal, pedido_id, producto_id, estado)
        VALUES (%s, %s, %s, %s, 'Pendiente')
        """
        
        sql_update_stock = "UPDATE Producto SET stock = stock - %s WHERE producto_id = %s"

        for prod in lista_productos:
            p_id = prod[0]
            cant = prod[1]
            precio = prod[2]
            subtotal = cant * precio
            
            # Guardar detalle
            cursor.execute(sql_detalle, (cant, subtotal, id_pedido_generado, p_id))
            
            # Descontar stock
            cursor.execute(sql_update_stock, (cant, p_id))
            
        # Si todo salio bien, guardamos cambios
        conexion.commit()
        return True
        
    except Exception as e:
        # Si algo falla, deshacemos todo para no dejar datos dañados
        conexion.rollback()
        print(f"Error critico al crear pedido: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def actualizarEstadoPedido(pedido_id, nuevo_estado):
    conexion = conectarBD()
    if not conexion: return False
    cursor = conexion.cursor()
    sql = "UPDATE Pedido SET estado = %s WHERE pedido_id = %s"
    try:
        cursor.execute(sql, (nuevo_estado, pedido_id))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error update pedido: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def eliminarPedido(pedido_id):
    conexion = conectarBD()
    if not conexion: return False
    cursor = conexion.cursor()
    
    # 1. Eliminar hijos: Detalle_Pedido
    sql_detalle = "DELETE FROM Detalle_Pedido WHERE pedido_id = %s"
    
    # 2. Eliminar hijos: Pago
    sql_pago = "DELETE FROM Pago WHERE pedido_id = %s"
    
    # 3. Eliminar padre: Pedido
    sql_pedido = "DELETE FROM Pedido WHERE pedido_id = %s"
    
    try:
        # Ejecutamos en orden
        cursor.execute(sql_detalle, (pedido_id,))
        cursor.execute(sql_pago, (pedido_id,)) # Borramos los pagos vinculados
        cursor.execute(sql_pedido, (pedido_id,))
        
        conexion.commit()
        return True
        
    except Exception as e:
        conexion.rollback() # Si falla, deshacemos todo para no dejar datos a medias
        print(f"Error al eliminar pedido (Constraint Pago/Detalle): {e}")
        return False
        
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()