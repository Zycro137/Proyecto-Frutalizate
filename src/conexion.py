import os
import mysql.connector as sql
from dotenv import load_dotenv

# Cargar variables de entorno una sola vez al importar el archivo
load_dotenv()

def conectarBD():
    connection = None
    
    # Intenta conectar a la base de datos, retorna el objeto de conexión si es exitoso, o None si falla.
    try:
        connection = sql.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME'),
            port = os.getenv('DB_PORT', 3306)
        )
        
        if connection.is_connected():
            return connection
        
    except sql.Error as e:
        print(f"Error al conectar con la base de datos (MySQL): {e}")
        return None

    except Exception as e:
        print(f"Error: {e}")
        return None