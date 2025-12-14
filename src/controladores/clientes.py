from datetime import date
from src.conexion import conectarBD

def buscarClienteSuscripcion(cedula):
    conexion = conectarBD()
    if not conexion:
        return None
    
    cursor = conexion.cursor()
    
    # MODIFICACION: Agregado ORDER BY y LIMIT 1.
    # Esto sirve para que, si el cliente tiene una suscripcion 'Cancelada' vieja
    # y una 'Activa' nueva (o viceversa), siempre obtengamos la mas reciente.
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

# --- (El resto de funciones: actualizarCliente, crearSuscripcion, cancelarSuscripcion se mantienen igual) ---
# Copia aqui las demas funciones que ya tenias (actualizarCliente, crearSuscripcion, cancelarSuscripcion)...
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