import psycopg2
from connection import get_connection

def crear_estructura():
    """
    Crea la estructura objeto-relacional e inserta los datos
    """
    commands = (
        # Borrado de tablas y tipos para limpiar la base de datos
        "DROP TABLE IF EXISTS ventas CASCADE;",
        "DROP TABLE IF EXISTS discos CASCADE;",
        "DROP TABLE IF EXISTS artistas CASCADE;",
        "DROP TYPE IF EXISTS sale_info CASCADE;",
        "DROP TYPE IF EXISTS artist_type CASCADE;",

        # Definición del tipo para artistas (nombre, apellido, nacionalidad)
        "CREATE TYPE artist_type AS (nombre VARCHAR(100), apellido VARCHAR(100), nacionalidad VARCHAR(100));",
        
        # Definición del tipo para ventas con el array de discos comprados
        "CREATE TYPE sale_info AS (customer_name VARCHAR(100), sale_date DATE, discos_comprados INTEGER[]);",

        # Creación de la tabla de artistas usando el tipo compuesto
        "CREATE TABLE artistas (id_artista SERIAL PRIMARY KEY, datos_artista artist_type);",
        
        # Creación de la tabla de discos con arrays para géneros y artistas
        "CREATE TABLE discos (id_disco SERIAL PRIMARY KEY, titulo VARCHAR(255), anio_lanzamiento INTEGER, generos TEXT[], artistas_ids INTEGER[]);",
        
        # Creación de la tabla de ventas usando el tipo compuesto
        "CREATE TABLE ventas (id_venta SERIAL PRIMARY KEY, detalles_venta sale_info);",

        # Inserción de los artistas solicitados
        "INSERT INTO artistas (datos_artista) VALUES (('Connor', 'Kauffman', 'Estadounidense'));",
        "INSERT INTO artistas (datos_artista) VALUES (('Rawayana', '', 'Venezolana'));",
        "INSERT INTO artistas (datos_artista) VALUES (('Neomai', '', 'Venezolana'));",

        # Inserción de discos de Connor Kauffman (ID 1)
        "INSERT INTO discos (titulo, anio_lanzamiento, generos, artistas_ids) VALUES ('Leavin You', 2023, ARRAY['Rock', 'Pop'], ARRAY[1]);",

        # Inserción de discos de Rawayana (ID 2)
        "INSERT INTO discos (titulo, anio_lanzamiento, generos, artistas_ids) VALUES ('Malportada', 2013, ARRAY['Reggae', 'Rock'], ARRAY[2]);",
        "INSERT INTO discos (titulo, anio_lanzamiento, generos, artistas_ids) VALUES ('Hora Loca', 2023, ARRAY['Reggae', 'Pop'], ARRAY[2]);",

        # Inserción de discos de Neomai (ID 3)
        "INSERT INTO discos (titulo, anio_lanzamiento, generos, artistas_ids) VALUES ('Carmesí', 2024, ARRAY['Indie', 'Rock'], ARRAY[3]);",
        "INSERT INTO discos (titulo, anio_lanzamiento, generos, artistas_ids) VALUES ('Síndrome de Stendhal', 2024, ARRAY['Indie', 'Alternative'], ARRAY[3]);",

        # Registro de una venta de prueba para los clientes que compra discos de Neomai y Rawayana
        "INSERT INTO ventas (detalles_venta) VALUES (('José Joselito', '2024-05-20', ARRAY[2, 4]));"
        "INSERT INTO ventas (detalles_venta) VALUES (('Mario el Castañas', '2025-01-23', ARRAY[1, 4, 5]));"
        "INSERT INTO ventas (detalles_venta) VALUES (('Inés Pérez', '2024-12-24', ARRAY[3]));"
    )

    conn = None
    try:
        # Abrir la conexión con el servidor PostgreSQL
        conn = get_connection()
        if conn is not None:
            cur = conn.cursor()
            # Ejecutar cada comando para montar la base de datos
            for command in commands:
                cur.execute(command)
            cur.close()
            # Guardar todos los cambios realizados
            conn.commit() 
            print("Base de datos configurada con los artistas y canciones solicitados.")
            
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error al cargar los datos: {error}")
        if conn:
            conn.rollback()
    finally:
        # Cerrar siempre la conexión al terminar
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    crear_estructura()