import psycopg2
from connection import get_connection

def insertar_artista_y_disco(nombre, apellido, nacionalidad, titulo, anio, generos):
    """ 
    Inserta un artista y su disco en una sola operación atómica. 
    Usa el ID generado del artista para asociarlo al array del disco.
    
    Args:
        nombre (str): Nombre del artista.
        apellido (str): Apellido del artista.
        nacionalidad (str): Nacionalidad del artista.
        titulo (str): Título del álbum o canción.
        anio (int): Año de lanzamiento.
        generos (list): Lista de géneros para el array de la base de datos.
        
    Returns:
        bool: True si la transacción se guardó (COMMIT), False si falló (ROLLBACK).
    """
    conn = get_connection()
    try:
        cur = conn.cursor()

        query_artista = """
            INSERT INTO artistas (datos_artista) 
            VALUES ((%s, %s, %s)) RETURNING id_artista;
        """
        cur.execute(query_artista, (nombre, apellido, nacionalidad))
        id_nuevo_artista = cur.fetchone()[0]

        query_disco = """
            INSERT INTO discos (titulo, anio_lanzamiento, generos, artistas_ids) 
            VALUES (%s, %s, %s, %s);
        """

        cur.execute(query_disco, (titulo, anio, generos, [id_nuevo_artista]))

        conn.commit()
        cur.close()
        return True
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"ERROR EN TRANSACCIÓN: {error}. Ejecutando ROLLBACK...")
        if conn:
            conn.rollback()
        return False
        
    finally:
        if conn:
            conn.close()

def rollback_duplicado():
    """ 
    Fuerza un error de clave duplicada para demostrar el ROLLBACK.
    Intenta insertar un artista 'Invisible', pero la transacción falla
    al intentar forzar un ID que ya existe (el ID 1).
    
    Args:
        None
        
    Returns:
        str: Resultado de la prueba.
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        
        # Este insert es válido y se queda en espera del commit
        print("Insertando artista 'Fantasma'...")
        cur.execute(
            "INSERT INTO artistas (datos_artista) VALUES ((%s, %s, %s));",
            ('Artista', 'Fantasma', 'Probablemente Colombiano')
        )
        
        # Forzamos el error: Intentamos insertar manualmente el ID 1, que ya está ocupado
        print("Forzando error: Intentando duplicar el ID 1...")
        cur.execute(
            "INSERT INTO artistas (id_artista, datos_artista) VALUES (1, (%s, %s, %s));",
            ('Error', 'Duplicado', 'N/A')
        )
        
        conn.commit()
        return "Error: La base de datos permitió un ID duplicado."
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"¡VIOLACIÓN DE CLAVE PRIMARIA!: {error}")
        # Al fallar aquí, el artista 'Fantasma' del Paso 1 se borra de la memoria
        if conn:
            conn.rollback()

        return "ROLLBACK EXITOSO: El 'Artista Fantasma' no se guardó."
        
    finally:
        if conn:
            conn.close()

def actualizar_discos_venta(id_venta, nuevos_ids_discos):
    """ 
    Actualiza la lista de canciones (array de IDs) de un pedido existente.
    
    Args:
        id_venta (int): ID del pedido a modificar.
        nuevos_ids_discos (list): Nueva lista de IDs de discos.
        
    Returns:
        bool: True si se realizó el COMMIT, False si hubo ROLLBACK.
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            UPDATE ventas 
            SET detalles_venta.discos_comprados = %s 
            WHERE id_venta = %s;
        """
        cur.execute(query, (nuevos_ids_discos, id_venta))
        
        if cur.rowcount == 0:
            conn.rollback()
            return False

        conn.commit()
        cur.close()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"❌ Error en la actualización de discos: {error}")
        if conn: conn.rollback()
        return False
    finally:
        if conn: conn.close()

def eliminar_venta(id_venta):
    """ 
    Elimina un pedido de la base de datos de forma atómica.
    
    Args:
        id_venta (int): ID de la venta a eliminar.
        
    Returns:
        bool: True si la eliminación fue exitosa, False en caso contrario.
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        
        query = "DELETE FROM ventas WHERE id_venta = %s;"
        cur.execute(query, (id_venta,))
        
        if cur.rowcount == 0:
            print(f"⚠️  No existe la venta con ID {id_venta}.")
            conn.rollback()
            return False

        conn.commit()
        cur.close()
        return True
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"❌ Error al eliminar: {error}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("--- TRANSACCIÓN EXITOSA: MICROTDH ---")
    exito = insertar_artista_y_disco(
        'MicroTDH', '', 'Venezolana', 
        'Otro 24', 2024, ['Rap', 'Reggaeton', 'Pop']
    )
    if exito:
        print("MicroTDH y 'Otro 24' guardados correctamente.")

    print("\n--- PRUEBA DE ROLLBACK (ID Duplicado) ---")
    print(rollback_duplicado())