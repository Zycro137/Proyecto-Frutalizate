from datetime import date
from src.conexion import conectarBD

def buscarClienteSuscripcion(cedula):
    conexion = conectarBD()
    if not conexion:
        return None
    
    cursor = conexion.cursor()
    
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
        datos = cursor.fetchone()
        return datos
        
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return None
        
    finally:
        if cursor: 
            cursor.close()
        if conexion: 
            conexion.close()

def actualizarCliente(cedula, nombre, apellido, telefono, email):
    conexion = conectarBD()
    if not conexion: return False
    cursor = conexion.cursor()
    sql = "UPDATE Cliente SET nombre=%s, apellido=%s, telefono=%s, email=%s WHERE cliente_id=%s"
    try:
        cursor.execute(sql, (nombre, apellido, telefono, email, cedula))
        conexion.commit()
        return True
    except Exception: return False
    finally: 
        if cursor: cursor.close() 
        if conexion: conexion.close()

def crearSuscripcion(cliente_id, frecuencia, fecha_prox):
    conexion = conectarBD()
    if not conexion: return False
    cursor = conexion.cursor()
    fecha_inicio = date.today()
    sql = "INSERT INTO Suscripcion (frecuencia, fecha_inicio, fecha_proxEntrega, estado, cliente_id) VALUES (%s, %s, %s, 'Activa', %s)"
    try:
        cursor.execute(sql, (frecuencia, fecha_inicio, fecha_prox, cliente_id))
        conexion.commit()
        return True
    except Exception: return False
    finally: 
        if cursor: cursor.close() 
        if conexion: conexion.close()

def cancelarSuscripcion(suscripcion_id):
    conexion = conectarBD()
    if not conexion: return False
    cursor = conexion.cursor()
    sql = "UPDATE Suscripcion SET estado = 'Cancelada' WHERE suscripcion_id = %s"
    try:
        cursor.execute(sql, (suscripcion_id,))
        conexion.commit()
        return True
    except Exception: return False
    finally: 
        if cursor: cursor.close() 
        if conexion: conexion.close()


# CRUD CLIENTES

def obtenerClientes():
    """Retorna una lista con todos los clientes registrados."""
    conexion = conectarBD()
    if not conexion: return []
    
    cursor = conexion.cursor()
    # Seleccionamos datos básicos
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

def crearCliente(cedula, nombre, apellido, telefono, email):
    conexion = conectarBD()
    if not conexion: return False
    
    cursor = conexion.cursor()
    sql = """
    INSERT INTO Cliente (cliente_id, nombre, apellido, telefono, email)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(sql, (cedula, nombre, apellido, telefono, email))
        conexion.commit()
        return True
    except Exception as e:
        # Esto captura si intentas meter una cédula repetida
        print(f"Error al crear cliente (Posible cédula duplicada): {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def eliminarCliente(cedula):
    conexion = conectarBD()
    if not conexion: return False
    
    cursor = conexion.cursor()
    # Esto falla si el cliente tiene suscripciones o pedidos (Integridad Referencial)
    sql = "DELETE FROM Cliente WHERE cliente_id = %s"
    
    try:
        cursor.execute(sql, (cedula,))
        conexion.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error al eliminar cliente (Revise si tiene historial de suscripciones/pedidos): {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()


# CRUD SUSCRIPCIONES

def obtenerTodasSuscripciones():
    """Retorna lista de todas las suscripciones con datos del cliente."""
    conexion = conectarBD()
    if not conexion: return []
    
    cursor = conexion.cursor()
    # Hacemos JOIN para ver el nombre del cliente y no solo su ID
    sql = """
    SELECT 
        s.suscripcion_id,
        c.nombre,
        c.apellido,
        s.frecuencia,
        s.fecha_proxEntrega,
        s.estado,
        s.cliente_id
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

def actualizarSuscripcion(sus_id, nueva_frec, nueva_fecha):
    conexion = conectarBD()
    if not conexion: return False
    cursor = conexion.cursor()
    
    sql = """
    UPDATE Suscripcion 
    SET frecuencia = %s, fecha_proxEntrega = %s
    WHERE suscripcion_id = %s
    """
    try:
        cursor.execute(sql, (nueva_frec, nueva_fecha, sus_id))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar suscripcion: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def eliminarSuscripcionFisica(sus_id):
    """Elimina el registro de la BD. Cuidado: Fallará si tiene pedidos."""
    conexion = conectarBD()
    if not conexion: return False
    cursor = conexion.cursor()
    
    sql = "DELETE FROM Suscripcion WHERE suscripcion_id = %s"
    try:
        cursor.execute(sql, (sus_id,))
        conexion.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error al eliminar suscripcion (Posiblemente tiene pedidos/detalles asociados): {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def obtenerSuscripcionPorId(id_sus):
    """Busca una suscripción específica para editarla."""
    conexion = conectarBD()
    if not conexion: return None
    cursor = conexion.cursor()
    
    # Obtenemos frecuencia y fecha para mostrarlas al usuario
    sql = "SELECT frecuencia, fecha_proxEntrega FROM Suscripcion WHERE suscripcion_id = %s"
    
    try:
        cursor.execute(sql, (id_sus,))
        return cursor.fetchone() # Retorna (frecuencia, fecha)
    except Exception as e:
        print(f"Error al buscar suscripcion: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()