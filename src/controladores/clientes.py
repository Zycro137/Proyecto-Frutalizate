from datetime import date
from src.conexion import conectarBD

def buscarClienteSuscripcion(cedula):
    conexion = conectarBD()
    if not conexion:
        return None
    
    cursor = conexion.cursor()
    
    # CORRECCION: Eliminamos c.direccion y agregamos s.direccion al final
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
        s.estado,
        s.direccion 
    FROM Cliente c
    LEFT JOIN Suscripcion s ON c.cliente_id = s.cliente_id
    WHERE c.cliente_id = %s
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
    if not conexion:
        return False
    
    cursor = conexion.cursor()
    sql = """
    UPDATE Cliente 
    SET nombre = %s, apellido = %s, telefono = %s, email = %s
    WHERE cliente_id = %s
    """
    try:
        cursor.execute(sql, (nombre, apellido, telefono, email, cedula))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar cliente: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def crearSuscripcion(cliente_id, frecuencia, direccion, fecha_prox):
    conexion = conectarBD()
    if not conexion:
        return False
    
    cursor = conexion.cursor()
    # Asumimos fecha de inicio hoy y estado Activa
    fecha_inicio = date.today()
    
    sql = """
    INSERT INTO Suscripcion (frecuencia, fecha_inicio, fecha_proxEntrega, estado, direccion, cliente_id)
    VALUES (%s, %s, %s, 'Activa', %s, %s)
    """
    try:
        cursor.execute(sql, (frecuencia, fecha_inicio, fecha_prox, direccion, cliente_id))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al crear suscripcion: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def cancelarSuscripcion(suscripcion_id):
    conexion = conectarBD()
    if not conexion:
        return False
    
    cursor = conexion.cursor()
    # Para el prototipo usamos DELETE para que se pueda volver a crear otra.
    # En un sistema real usarias UPDATE estado = 'Cancelada'
    sql = "DELETE FROM Suscripcion WHERE suscripcion_id = %s"
    
    try:
        cursor.execute(sql, (suscripcion_id,))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al cancelar suscripcion: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

