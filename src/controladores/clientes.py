from datetime import date
from src.conexion import conectarBD
import mysql.connector


def buscarClienteSuscripcion(cedula):
    conexion = conectarBD()
    if not conexion: return None
    
    cursor = conexion.cursor()
    # Mantenemos el LEFT JOIN ya que la Vista 'reporte_suscripciones' filtra solo activas
    # y aquí necesitamos ver al cliente aunque no tenga suscripción.
    sql = """
    SELECT 
        c.nombre, 
        c.apellido, 
        c.cliente_id, 
        c.telefono, 
        c.email,
        s.suscripcion_id, 
        s.frecuencia, 
        s.fecha_proxEntrega,
        s.estado
    FROM Cliente c
    LEFT JOIN Suscripcion s ON c.cliente_id = s.cliente_id
    WHERE c.cliente_id = %s
    ORDER BY s.suscripcion_id DESC
    LIMIT 1
    """
    try:
        cursor.execute(sql, (cedula,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def obtenerClientes():
    """Retorna una lista con todos los clientes registrados."""
    conexion = conectarBD()
    if not conexion: return []
    cursor = conexion.cursor()
    sql = "SELECT cliente_id, nombre, apellido, telefono, email FROM Cliente"
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al listar clientes: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def obtenerTodasSuscripciones():
    """Retorna lista de todas las suscripciones."""
    conexion = conectarBD()
    if not conexion: return []
    cursor = conexion.cursor()
    sql = """
    SELECT s.suscripcion_id, c.nombre, c.apellido, s.frecuencia, 
           s.fecha_proxEntrega, s.estado, s.cliente_id
    FROM Suscripcion s
    JOIN Cliente c ON s.cliente_id = c.cliente_id
    ORDER BY s.suscripcion_id DESC
    """
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al listar suscripciones: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def obtenerSuscripcionPorId(id_sus):
    conexion = conectarBD()
    if not conexion: return None
    cursor = conexion.cursor()
    sql = "SELECT frecuencia, fecha_proxEntrega FROM Suscripcion WHERE suscripcion_id = %s"
    try:
        cursor.execute(sql, (id_sus,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error al buscar suscripcion: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

# --- ESCRITURA CON STORED PROCEDURES ---

def crearCliente(cedula, nombre, apellido, telefono, email):
    conexion = conectarBD()
    if not conexion: return False
    cursor = conexion.cursor()
    
    try:
        # SP: insertCliente(p_id, p_nombre, p_apellido, p_telefono, p_email)
        cursor.callproc('insertCliente', [cedula, nombre, apellido, telefono, email])
        conexion.commit()
        return True
        
    except mysql.connector.Error as err:
        # Capturamos el SIGNAL SQLSTATE '45000' del SP si ocurre error
        print(f"Error BD: {err.msg}") 
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def actualizarCliente(cedula, nombre, apellido, telefono, email):
    conexion = conectarBD()
    if not conexion: return False
    cursor = conexion.cursor()
    
    try:
        # El SP updateCliente tiene este orden: p_id, p_telefono, p_email, p_nombre, p_apellido
        cursor.callproc('updateCliente', [cedula, telefono, email, nombre, apellido])
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

def eliminarCliente(cedula):
    conexion = conectarBD()
    if not conexion: return False
    cursor = conexion.cursor()
    
    try:
        # SP: deleteCliente(p_id)
        cursor.callproc('deleteCliente', [cedula])
        conexion.commit()
        return True
        
    except mysql.connector.Error as err:
        # Aquí saltará si tiene deudas/pedidos gracias al SIGNAL del SP
        print(f"Error BD: {err.msg}")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def crearSuscripcion(cliente_id, frecuencia, fecha_prox):
    conexion = conectarBD()
    if not conexion: return False
    cursor = conexion.cursor()
    
    try:
        # SP: insertSuscripcion(p_cliente_id, p_frecuencia, p_fecha_prox)
        cursor.callproc('insertSuscripcion', [cliente_id, frecuencia, fecha_prox])
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

def actualizarSuscripcion(sus_id, nueva_frec, nueva_fecha):
    conexion = conectarBD()
    if not conexion: return False
    cursor = conexion.cursor()
    
    try:
        # SP: updateSuscripcion(p_sus_id, p_frecuencia, p_fecha_prox)
        cursor.callproc('updateSuscripcion', [sus_id, nueva_frec, nueva_fecha])
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

def eliminarSuscripcionFisica(sus_id):
    conexion = conectarBD()
    if not conexion: return False
    cursor = conexion.cursor()
    
    try:
        # SP: eliminarSuscripcion(p_sus_id)
        cursor.callproc('eliminarSuscripcion', [sus_id])
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

def cancelarSuscripcion(suscripcion_id):
    """
    NOTA: No existe Stored Procedure para 'Cancelar' (Update Estado), 
    así que mantenemos el SQL directo o deberíamos pedir al equipo agregarlo.
    Por ahora se mantiene la lógica SQL directa.
    """
    conexion = conectarBD()
    if not conexion: return False
    cursor = conexion.cursor()
    sql = "UPDATE Suscripcion SET estado = 'Cancelada' WHERE suscripcion_id = %s"
    try:
        cursor.execute(sql, (suscripcion_id,))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al cancelar: {e}")
        return False
    finally: 
        if cursor: cursor.close() 
        if conexion: conexion.close()


def obtenerReporteSuscripcionesVista():
    """Usa la VISTA reporte_suscripciones creada por el grupo 3"""
    conexion = conectarBD()
    if not conexion: return []
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT * FROM reporte_suscripciones")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error reporte: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()