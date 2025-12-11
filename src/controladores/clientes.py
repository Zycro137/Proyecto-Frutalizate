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