from datetime import date
from src.conexion import conectarBD
import mysql.connector

# --- LECTURAS ---

def obtenerPedidos():
    """
    Devuelve historial de pedidos.
    Mantenemos el SQL original con JOINs en lugar de la Vista 'reporte_PedidosCliente',
    porque la Vista usa INNER JOIN con Pago, lo que ocultaría los pedidos 'Pendientes'
    que aún no tienen pago registrado.
    """
    conexion = conectarBD()
    if not conexion: return []
    cursor = conexion.cursor()
    
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
    """
    Aquí podríamos usar la Vista 'reporte_DetallePedido' si filtramos por ID.
    """
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

# --- CRUD PEDIDOS CON STORED PROCEDURES ---

def crearPedidoCompleto(cliente_id, repartidor_id, direccion, hora, lista_productos):
    """
    Usa el SP 'insertPedido' y confía en el Trigger para descontar stock.
    """
    conexion = conectarBD()
    if not conexion: return False
    cursor = conexion.cursor()
    
    id_pedido_generado = None

    try:
        # 1. Llamar al SP para insertar el ENCABEZADO
        # Parametros SP: p_fecha, p_hora, p_direccion, p_cliente, p_repartidor
        fecha_hoy = date.today()
        
        cursor.callproc('insertPedido', [fecha_hoy, hora, direccion, cliente_id, repartidor_id])
        
        # NOTA: El SP hace commit interno. Necesitamos el ID generado.
        cursor.execute("SELECT LAST_INSERT_ID()")
        row = cursor.fetchone()
        if row:
            id_pedido_generado = row[0]
        
        if not id_pedido_generado:
            raise Exception("No se pudo obtener el ID del pedido creado.")

        # 2. Insertar DETALLES (Tabla Detalle_Pedido)
        
        sql_detalle = """
        INSERT INTO Detalle_Pedido (cantidad, subtotal, pedido_id, producto_id, estado)
        VALUES (%s, %s, %s, %s, 'Pendiente')
        """
        
        for prod in lista_productos:
            p_id = prod[0]
            cant = prod[1]
            precio = prod[2]
            subtotal = cant * precio
            
            # Solo insertamos. La BD hace el resto
            cursor.execute(sql_detalle, (cant, subtotal, id_pedido_generado, p_id))
            
        conexion.commit()
        return True
        
    except mysql.connector.Error as err:
        # Si falla el SP o el Trigger, capturamos el mensaje SIGNAL
        print(f"Error BD: {err.msg}")
        
        # ROLLBACK MANUAL:
        # Si fallaron los detalles, el encabezado ya se creó (por el commit del SP).
        # Intentamos borrarlo para no dejar basura.
        if id_pedido_generado:
            try:
                cursor.callproc('deletePedido', [id_pedido_generado])
                conexion.commit()
                print(" -> Se revirtió la creación del pedido.")
            except:
                pass
        return False

    except Exception as e:
        print(f"Error critico al crear pedido: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def actualizarEstadoPedido(pedido_id, nuevo_estado):
    conexion = conectarBD()
    if not conexion: return False
    cursor = conexion.cursor()
    
    try:
        # SP: updateEstadoPedido(p_id, p_estado)
        cursor.callproc('updateEstadoPedido', [pedido_id, nuevo_estado])
        conexion.commit()
        return True
        
    except mysql.connector.Error as err:
        print(f"Error BD: {err.msg}")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def eliminarPedido(pedido_id):
    conexion = conectarBD()
    if not conexion: return False
    cursor = conexion.cursor()
    
    try:
        # 1. Limpieza de hijos manual (Ya que no hay SP para detalles/pagos)
        # Esto asegura que el SP deletePedido no falle por Foreign Key
        sql_detalle = "DELETE FROM Detalle_Pedido WHERE pedido_id = %s"
        sql_pago = "DELETE FROM Pago WHERE pedido_id = %s"
        
        cursor.execute(sql_detalle, (pedido_id,))
        cursor.execute(sql_pago, (pedido_id,))
        
        # 2. Llamar al SP para eliminar el PADRE
        # SP: deletePedido(p_id)
        cursor.callproc('deletePedido', [pedido_id])
        
        conexion.commit()
        return True
        
    except mysql.connector.Error as err:
        conexion.rollback()
        print(f"Error BD: {err.msg}")
        return False
    except Exception as e:
        conexion.rollback()
        print(f"Error al eliminar pedido: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def obtenerReportePedidosCliente():
    """Usa la VISTA reporte_PedidosCliente"""
    conexion = conectarBD()
    if not conexion: return []
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT * FROM reporte_PedidosCliente")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error reporte: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def obtenerReporteDetallePedido():
    """Usa la VISTA reporte_DetallePedido"""
    conexion = conectarBD()
    if not conexion: return []
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT * FROM reporte_DetallePedido ORDER BY pedido_id DESC")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error reporte: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()