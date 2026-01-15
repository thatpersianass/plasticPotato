import psycopg2
from connection import get_connection

# --- CONSULTAS DE BÚSQUEDA GENERAL ---

def listar_todos_artistas():
    """ 
    Recupera la lista completa de artistas desglosando el tipo compuesto 'artist_type'.
    
    Args:
        None
        
    Returns:
        list: Lista de tuplas con (id_artista, nombre, apellido, nacionalidad).
    """
    conn = get_connection()
    resultados = []

    try:
        cur = conn.cursor()
        query = """
            SELECT id_artista, 
                (datos_artista).nombre, 
                (datos_artista).apellido, 
                (datos_artista).nacionalidad 
            FROM artistas ORDER BY id_artista;
        """
        cur.execute(query)
        resultados = cur.fetchall()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error al listar artistas: {error}")

    finally:
        if conn: conn.close()

    return resultados

def listar_todos_discos():
    """ 
    Recupera todos los discos almacenados, incluyendo sus arrays de géneros y artistas.
    
    Args:
        None
        
    Returns:
        list: Lista de tuplas con (id_disco, titulo, anio, generos, artistas_ids).
    """

    conn = get_connection()
    resultados = []

    try:
        cur = conn.cursor()
        query = "SELECT id_disco, titulo, anio_lanzamiento, generos, artistas_ids FROM discos ORDER BY id_disco;"
        cur.execute(query)
        resultados = cur.fetchall()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error al listar discos: {error}")

    finally:
        if conn: conn.close()

    return resultados

def listar_todas_ventas():
    """ 
    Recupera el historial de ventas desglosando el tipo compuesto 'sale_info'.
    
    Args:
        None
        
    Returns:
        list: Lista de tuplas con (id_venta, cliente, fecha, discos_ids).
    """
    conn = get_connection()
    resultados = []

    try:
        cur = conn.cursor()
        query = """
            SELECT id_venta, 
                (detalles_venta).customer_name, 
                (detalles_venta).sale_date, 
                (detalles_venta).discos_comprados 
            FROM ventas ORDER BY id_venta;
        """
        cur.execute(query)
        resultados = cur.fetchall()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error al listar ventas: {error}")

    finally:
        if conn: conn.close()

    return resultados

# --- CONSULTAS DE BÚSQUEDA ESPECÍFICA ---

def consulta_generos(genero):
    """ 
    Busca los discos de un género específico y devuelve sus datos.
    
    Args:
        genero (str): Nombre del género musical.
        
    Returns:
        list: Lista de tuplas con (titulo, anio_lanzamiento).
    """
    conn = get_connection()
    resultados = []

    try:
        cur = conn.cursor()
        query = "SELECT titulo, anio_lanzamiento FROM discos WHERE %s = ANY(generos);"
        cur.execute(query, (genero,))
        resultados = cur.fetchall()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error al consultar géneros: {error}")

    finally:
        if conn: conn.close()

    return resultados

def consulta_cliente(nombre_cliente):
    """ 
    Obtiene los discos comprados por un cliente desde el tipo compuesto 'sale_info'.
    
    Args:
        nombre_cliente (str): Nombre del cliente.
        
    Returns:
        list: Lista de tuplas con los títulos de los discos.
    """
    conn = get_connection()
    resultados = []

    try:
        cur = conn.cursor()
        query = """
            SELECT d.titulo 
            FROM discos d
            JOIN ventas v ON d.id_disco = ANY((v.detalles_venta).discos_comprados)
            WHERE (v.detalles_venta).customer_name = %s;
        """
        cur.execute(query, (nombre_cliente,))
        resultados = cur.fetchall()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error al consultar cliente: {error}")

    finally:
        if conn: conn.close()

    return resultados

def consulta_colaboradores(titulo_disco):
    """ 
    Devuelve los artistas de un disco extrayendo datos del tipo compuesto 'artist_type'.
    
    Args:
        titulo_disco (str): Título del disco.
        
    Returns:
        list: Lista de tuplas con (nombre, apellido) de los artistas.
    """
    conn = get_connection()
    resultados = []

    try:
        cur = conn.cursor()
        query = """
            SELECT (a.datos_artista).nombre, (a.datos_artista).apellido
            FROM artistas a
            JOIN discos d ON a.id_artista = ANY(d.artistas_ids)
            WHERE d.titulo = %s;
        """
        cur.execute(query, (titulo_disco,))
        resultados = cur.fetchall()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error al consultar colaboradores: {error}")

    finally:
        if conn: conn.close()

    return resultados

def buscar_disco_por_id(id_disco):
    """ 
    Busca la información detallada de un disco por su ID.
    
    Args:
        id_disco (int): ID único del disco.
        
    Returns:
        tuple: Tupla con los datos del disco o None si no existe.
    """
    conn = get_connection()
    resultado = None

    try:
        cur = conn.cursor()
        query = "SELECT * FROM discos WHERE id_disco = %s;"
        cur.execute(query, (id_disco,))
        resultado = cur.fetchone()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error al buscar disco por ID: {error}")

    finally:
        if conn: conn.close()

    return resultado

def obtener_lista_generos():
    """ 
    Extrae todos los géneros únicos almacenados en los arrays de la tabla discos.
    
    Returns:
        list: Lista de strings con los géneros únicos.
    """
    conn = get_connection()
    resultados = []
    try:
        cur = conn.cursor()
        # unnest expande el array en filas para poder usar DISTINCT
        query = "SELECT DISTINCT unnest(generos) FROM discos ORDER BY 1;"
        cur.execute(query)
        # Convertimos la lista de tuplas en una lista simple de strings
        resultados = [r[0] for r in cur.fetchall()]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error al obtener géneros: {error}")
    finally:
        if conn: conn.close()
    return resultados

def obtener_lista_clientes():
    """ 
    Extrae los nombres únicos de los clientes desde el tipo compuesto de ventas.
    
    Returns:
        list: Lista de nombres de clientes.
    """
    conn = get_connection()
    resultados = []
    try:
        cur = conn.cursor()
        query = "SELECT DISTINCT (detalles_venta).customer_name FROM ventas ORDER BY 1;"
        cur.execute(query)
        resultados = [r[0] for r in cur.fetchall()]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error al obtener clientes: {error}")
    finally:
        if conn: conn.close()
    return resultados

def obtener_lista_titulos_discos():
    """ 
    Obtiene todos los títulos de los discos disponibles en el catálogo.
    
    Returns:
        list: Lista de títulos de discos.
    """
    conn = get_connection()
    resultados = []
    try:
        cur = conn.cursor()
        query = "SELECT titulo FROM discos ORDER BY titulo;"
        cur.execute(query)
        resultados = [r[0] for r in cur.fetchall()]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error al obtener títulos: {error}")
    finally:
        if conn: conn.close()
    return resultados

def obtener_discos_id_y_titulo():
    """ 
    Obtiene el ID y el título de todos los discos para permitir la selección por ID.
    
    Returns:
        list: Lista de tuplas (id_disco, titulo).
    """
    conn = get_connection()
    resultados = []
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_disco, titulo FROM discos ORDER BY id_disco;")
        resultados = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"❌ Error al obtener catálogo: {error}")
    finally:
        if conn: conn.close()
    return resultados

if __name__ == "__main__":
    print("--- LISTADO DE ARTISTAS (ID, Nombre, Apellido, Nacionalidad) ---")
    artistas = listar_todos_artistas()
    for art in artistas:
        print(art)

    print("\n--- DISCOS DE GÉNERO 'Rock' ---")
    discos_rock = consulta_generos('Rock')
    for disco in discos_rock:
        # Cada 'disco' es una tupla (titulo, anio)
        print(f"Título: {disco[0]} | Año: {disco[1]}")

    print("\n--- COMPRAS DE JUAN PÉREZ ---")
    compras = consulta_cliente('Juan Pérez')
    if compras:
        for item in compras:
            print(f"Compró: {item[0]}")
    else:
        print("No hay compras registradas para este cliente.")

    cancion = 'Carmesí'
    print(f"\n--- COLABORADORES EN '{cancion}' ---")
    colaboradores = consulta_colaboradores(cancion)
    for colab in colaboradores:
        print(f"Artista: {colab[0]} {colab[1]}")
        

    print("\n--- BUSCANDO DISCO CON ID 2 ---")
    disco_especifico = buscar_disco_por_id(2)
    if disco_especifico:
        print(f"Resultado: {disco_especifico}")